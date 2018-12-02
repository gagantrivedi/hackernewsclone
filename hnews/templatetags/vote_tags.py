from django import template

from hnews.models import Post

register = template.Library()


@register.filter
def is_upvoted(post, user):
    return user in post.votes.all()
