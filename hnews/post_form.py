from django.forms import ModelForm
from hnews.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['hn_post_id', 'rank_is_expired', 'total_votes', 'total_comments', 'rank']
