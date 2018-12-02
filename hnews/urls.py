from django.conf.urls import url

from hnews.views import PostListView, AddPostView, vote_view, PostDetailView


urlpatterns = [

    url('^$', PostListView.as_view(), name='home'),
    url('^create/$', AddPostView.as_view(), name='create_post'),
    url('^vote/$', vote_view, name='vote'),
    url('^post/(?P<pk>\d+)/$', PostDetailView.as_view(), name='details'),



]
