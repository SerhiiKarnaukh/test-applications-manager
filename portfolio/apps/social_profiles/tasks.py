from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from .models import Profile, FriendshipRequest


@shared_task
def create_social_friend_suggestions():
    users = Profile.objects.all()

    for user in users:
        user.people_you_may_know.clear()

        for friend in user.friends.all():
            print('Is friend with:', friend)

            for friends_friend in friend.friends.all():
                if friends_friend not in user.friends.all() and friends_friend != user:
                    user.people_you_may_know.add(friends_friend)


@shared_task
def delete_old_rejected_friendship_requests():
    one_week_ago = timezone.now() - timedelta(days=7)

    old_rejected_requests = FriendshipRequest.objects.filter(
        status=FriendshipRequest.REJECTED,
        created_at__lt=one_week_ago
    )

    old_rejected_requests.delete()
