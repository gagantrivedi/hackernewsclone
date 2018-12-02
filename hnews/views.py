# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from hnews.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'posts_list.html'
    paginate_by = 30

    def get_queryset(self):
        if 'search' in self.request.GET:
            search_query = self.request.GET['search']
            vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            query = SearchQuery(search_query)
            return Post.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')


        else:
            return Post.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListView, self).get_context_data(**kwargs)
        current_page = self.request.GET.get('page', 1)
        context['post_rank'] = int(current_page) * 30 - 29
        return context


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'url', 'description']
    success_url = '/'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_comments.html'


@login_required()
def vote_view(request):
    post_id = request.GET.get('post_id')
    action = request.GET.get('action')
    post = Post.objects.filter(id=post_id).first()
    if post:
        if action == 'upvote' and request.user not in post.votes.all():

            post.votes.add(request.user)
            post.total_votes = post.total_votes + 1
        elif request.user in post.votes.all():
            post.votes.remove(request.user)
            post.total_votes = post.total_votes - 1
        post.save()
        return HttpResponseRedirect('/')

    else:
        messages.error(request, 'Wrong post id')
        return HttpResponseRedirect('/')
