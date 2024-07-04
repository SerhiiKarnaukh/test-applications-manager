import uuid

from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.timesince import timesince

from social_profiles.models import Profile


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(Profile,
                                   related_name='likes',
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Profile,
                                   related_name='comments',
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )

    def created_at_formatted(self):
        return timesince(self.created_at)


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

    is_private = models.BooleanField(default=False)

    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile,
                                   related_name='posts',
                                   on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at', )

    def created_at_formatted(self):
        return timesince(self.created_at)


class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()
