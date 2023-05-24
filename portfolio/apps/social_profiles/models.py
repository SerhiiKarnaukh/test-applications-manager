import uuid
from django.db import models
from accounts.models import Account

from .utils import get_random_code
from django.template.defaultfilters import slugify


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio...", max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='social/avatars/avatar.png',
                               upload_to='social/avatars/')
    friends = models.ManyToManyField('self')
    friends_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def save(self, *args, **kwargs):
        if self.first_name == "":
            self.first_name = self.user.first_name
        if self.last_name == "":
            self.last_name = self.user.last_name
        if self.email == "":
            self.email = self.user.email

        if self.pk is None:  # new instance, always create slug
            self.create_slug()
        else:
            old_instance = Profile.objects.get(pk=self.pk)
            if (self.first_name != old_instance.first_name
                    or self.last_name != old_instance.last_name):
                self.create_slug()
        super().save(*args, **kwargs)

    def create_slug(self):
        if self.first_name and self.last_name:
            to_slug = slugify(f"{self.first_name}-{self.last_name}")
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(f"{to_slug}-{get_random_code()}")
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user.username)
        self.slug = to_slug


class FriendshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(Profile,
                                    related_name='received_friendshiprequests',
                                    on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile,
                                   related_name='created_friendshiprequests',
                                   on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=SENT)
