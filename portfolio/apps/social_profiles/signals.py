from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Profile


@receiver(pre_save, sender=Profile)
def delete_old_avatar(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = Profile.objects.get(pk=instance.pk).avatar
        except Profile.DoesNotExist:
            return

        new_avatar = instance.avatar
        if old_avatar and old_avatar != new_avatar and old_avatar.name != 'social/avatars/avatar.png':
            old_avatar.delete(save=False)


# @receiver(post_save, sender=Relationship)
# def post_save_add_to_friends(sender, instance, created, **kwargs):
#     sender_ = instance.sender
#     receiver_ = instance.receiver
#     if instance.status == 'accepted':
#         sender_.friends.add(receiver_.user)
#         receiver_.friends.add(sender_.user)
#         sender_.save()
#         receiver_.save()

# @receiver(pre_delete, sender=Relationship)
# def pre_delete_remove_from_friends(sender, instance, **kwargs):
#     sender = instance.sender
#     receiver = instance.receiver
#     sender.friends.remove(receiver.user)
#     receiver.friends.remove(sender.user)
#     sender.save()
#     receiver.save()
