from celery import shared_task

from .models import Profile


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
