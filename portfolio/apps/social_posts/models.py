import uuid

from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.timesince import timesince

from social_profiles.models import Profile


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to='social/posts',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True)
    created_by = models.ForeignKey(Profile,
                                   related_name='post_attachments',
                                   on_delete=models.CASCADE)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    attachments = models.ManyToManyField(PostAttachment, blank=True)

    # likes
    # likes_count

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile,
                                   related_name='posts',
                                   on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at', )

    def created_at_formatted(self):
        return timesince(self.created_at)
