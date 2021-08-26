from django.db.models import Count
from .models import Tag, Post
import random


def get_tags():
    return Tag.objects.annotate(cnt=Count('post')).filter(cnt__gt=0)


def get_latest_posts():
    return Post.published.all().order_by('-publish')[:4]


def get_random_article():
    post = list(Post.published.all())
    post = random.sample(post, 1)
    return post
