# -*- coding: utf-8 -*-

import django
import os
import sys

from datetime import timedelta
from collections import Counter
from django.utils import timezone

sys.path.append(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")
django.setup()

from social_posts.models import Post, Trend


def extract_hashtags(text, trends):
    for word in text.split():
        if len(word) > 1 and word[0] == '#':
            hashtag = word[1:]
            trends.append(hashtag)

    return trends


for trend in Trend.objects.all():
    trend.delete()

trends = []
this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
twenty_four_hours = this_hour - timedelta(hours=24)

for post in Post.objects.filter(created_at__gte=twenty_four_hours):
    extract_hashtags(post.body, trends),

if not trends:
    all_posts = Post.objects.all().order_by('-created_at')
    for post in all_posts:
        extract_hashtags(post.body, trends)
        if len(trends) >= 5:
            break

for trend in Counter(trends).most_common(10):
    Trend.objects.create(hashtag=trend[0], occurences=trend[1])
