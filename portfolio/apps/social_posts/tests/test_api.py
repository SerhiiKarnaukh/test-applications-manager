from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from social_profiles.models import Profile
from social_posts.models import Post
from core.utils import create_active_user


class PostListApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = create_active_user(
            email="testuser@example.com",
            username="testuser",
            password="pass123",
            first_name="Test",
            last_name="User"
        )
        self.profile = Profile.objects.create(user=self.user)

        self.friend = create_active_user(
            email="friend@example.com",
            username="friend",
            password="pass123",
            first_name="Friend",
            last_name="User"
        )
        self.friend_profile = Profile.objects.create(user=self.friend)
        self.profile.friends.add(self.friend_profile)

        Post.objects.create(body="Hello #test", created_by=self.friend_profile, is_private=False)
        Post.objects.create(body="Only visible to friends", created_by=self.profile, is_private=True)
        Post.objects.create(body="Public post", created_by=self.friend_profile, is_private=False)

    def test_post_list_without_trend(self):
        self.client.login(username="testuser@example.com", password="pass123")
        response = self.client.get(reverse("social_posts:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertTrue(any("Public post" in p["body"] for p in response.data["results"]["posts"]))

    def test_post_list_with_trend(self):
        self.client.login(username="testuser@example.com", password="pass123")

        response = self.client.get(reverse("social_posts:post_list"), {"trend": "test"})
        self.assertEqual(response.status_code, 200)

        bodies = [p["body"] for p in response.data["results"]["posts"]]
        self.assertIn(
            "Hello #test",
            bodies,
            msg="Expected post with body 'Hello #test' not found in trend-based response"
        )


class PostDetailApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = create_active_user(
            email="user@example.com",
            username="user",
            password="pass123",
            first_name="User",
            last_name="Test"
        )
        self.profile = Profile.objects.create(user=self.user)

        self.friend = create_active_user(
            email="friend@example.com",
            username="friend",
            password="pass123",
            first_name="Friend",
            last_name="User"
        )
        self.friend_profile = Profile.objects.create(user=self.friend)
        self.profile.friends.add(self.friend_profile)

        self.post_by_friend = Post.objects.create(
            body="Friend's public post", created_by=self.friend_profile, is_private=False
        )

        self.private_post_by_self = Post.objects.create(
            body="Private post by self", created_by=self.profile, is_private=True
        )

        self.public_post = Post.objects.create(
            body="Public post", created_by=self.profile, is_private=False
        )

    def test_user_sees_friends_public_post(self):
        self.client.login(username="user@example.com", password="pass123")
        url = reverse("social_posts:post_detail", args=[self.post_by_friend.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["post"]["body"], "Friend's public post")

    def test_user_sees_own_private_post(self):
        self.client.login(username="user@example.com", password="pass123")
        url = reverse("social_posts:post_detail", args=[self.private_post_by_self.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["post"]["body"], "Private post by self")

    def test_anonymous_user_sees_public_post(self):
        url = reverse("social_posts:post_detail", args=[self.public_post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["post"]["body"], "Public post")
