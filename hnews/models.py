# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='my_posts')
    total_votes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField()
    hn_rank = models.PositiveSmallIntegerField(default=1)
    rank_is_expired = models.BooleanField(default=False)
    hn_post_id = models.IntegerField(null=True, blank=True)
    votes = models.ManyToManyField(User)
    slug=models.SlugField(default=title)


    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super(Post, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hnews_post'
        ordering = ['-rank_is_expired', '-hn_rank']
