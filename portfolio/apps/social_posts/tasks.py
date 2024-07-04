from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from collections import Counter

from .models import Post, Trend


@shared_task
def create_social_posts_trends():
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

    for post in Post.objects.filter(created_at__gte=twenty_four_hours).filter(is_private=False):
        extract_hashtags(post.body, trends)

    if not trends:
        all_posts = Post.objects.filter(is_private=False).order_by('-created_at')
        for post in all_posts:
            extract_hashtags(post.body, trends)
            if len(trends) >= 5:
                break

    for trend in Counter(trends).most_common(10):
        Trend.objects.create(hashtag=trend[0], occurences=trend[1])
