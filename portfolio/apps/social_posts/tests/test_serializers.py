import os
import tempfile
from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory

from social_profiles.models import Profile
from social_posts.models import PostAttachment
from social_posts.serializers import PostAttachmentSerializer
from core.utils import create_test_image, create_active_user


@override_settings(MEDIA_ROOT=os.path.join(tempfile.gettempdir(), "test_media"))
class PostAttachmentSerializerTest(TestCase):
    def setUp(self):
        self.image_dir = os.path.join(tempfile.gettempdir(), "test_media", "social", "posts")

        self.user = create_active_user(
            email="user@example.com",
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        self.profile = Profile.objects.create(user=self.user)

        self.image = create_test_image("test-image.jpg")

    def tearDown(self):
        media_root = os.path.join(tempfile.gettempdir(), "test_media")
        if os.path.exists(media_root):
            for root, dirs, files in os.walk(media_root, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(media_root)

    def test_image_url_is_correct(self):
        attachment = PostAttachment.objects.create(
            image=self.image,
            created_by=self.profile
        )

        request = APIRequestFactory().get("/dummy-url")
        serializer = PostAttachmentSerializer(instance=attachment, context={"request": request})
        data = serializer.data

        self.assertEqual(set(data.keys()), {"id", "image_url"})
        self.assertIsNotNone(data["image_url"])
        self.assertIn("social/posts/test-image", data["image_url"])

    def test_image_url_is_none_if_no_image(self):
        attachment = PostAttachment.objects.create(
            created_by=self.profile
        )

        request = APIRequestFactory().get("/dummy-url")
        serializer = PostAttachmentSerializer(instance=attachment, context={"request": request})
        data = serializer.data

        self.assertEqual(set(data.keys()), {"id", "image_url"})
        self.assertIsNone(data["image_url"])
