import os
import tempfile
from django.test import TestCase, override_settings

from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient

from social_profiles.models import Profile, FriendshipRequest
from social_posts.models import Post, PostAttachment, Like, Comment, Trend

from core.utils import create_active_user, create_test_image


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


class PostListProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.author_user = create_active_user(
            email="author@example.com",
            username="author",
            password="pass123",
            first_name="Author",
            last_name="User",
        )
        self.author_profile = Profile.objects.create(user=self.author_user)

        self.friend_user = create_active_user(
            email="friend@example.com",
            username="friend",
            password="pass123",
            first_name="Friend",
            last_name="User",
        )
        self.friend_profile = Profile.objects.create(user=self.friend_user)

        self.stranger_user = create_active_user(
            email="stranger@example.com",
            username="stranger",
            password="pass123",
            first_name="Stranger",
            last_name="User",
        )
        self.stranger_profile = Profile.objects.create(user=self.stranger_user)

        self.public_post = Post.objects.create(body="Public", created_by=self.author_profile, is_private=False)
        self.private_post = Post.objects.create(body="Private", created_by=self.author_profile, is_private=True)

    def test_authenticated_friend_sees_all_posts(self):
        self.client.login(username="friend@example.com", password="pass123")
        self.friend_profile.friends.add(self.author_profile)

        url = reverse("social_posts:post_list_profile", args=[self.author_profile.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        posts = response.json()["results"]["posts"]
        bodies = [p["body"] for p in posts]
        self.assertIn("Public", bodies)
        self.assertIn("Private", bodies)
        self.assertEqual(response.json()["results"]["can_send_friendship_request"], False)

    def test_authenticated_stranger_sees_only_public(self):
        self.client.login(username="stranger@example.com", password="pass123")

        url = reverse("social_posts:post_list_profile", args=[self.author_profile.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        posts = response.json()["results"]["posts"]
        bodies = [p["body"] for p in posts]
        self.assertIn("Public", bodies)
        self.assertNotIn("Private", bodies)
        self.assertEqual(response.json()["results"]["can_send_friendship_request"], True)

    def test_unauthenticated_user_sees_only_public(self):
        url = reverse("social_posts:post_list_profile", args=[self.author_profile.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        posts = response.json()["results"]["posts"]
        bodies = [p["body"] for p in posts]
        self.assertIn("Public", bodies)
        self.assertNotIn("Private", bodies)
        self.assertEqual(response.json()["results"]["can_send_friendship_request"], False)

    def test_rejected_friend_request_sets_flag(self):
        self.client.login(username="stranger@example.com", password="pass123")

        FriendshipRequest.objects.create(
            created_by=self.stranger_profile,
            created_for=self.author_profile,
            status='rejected'
        )

        url = reverse("social_posts:post_list_profile", args=[self.author_profile.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        posts = response.json()["results"]["posts"]
        bodies = [p["body"] for p in posts]

        self.assertIn("Public", bodies)
        self.assertNotIn("Private", bodies)
        self.assertEqual(response.json()["results"]["can_send_friendship_request"], "rejected")

    def test_rejected_friend_request_from_profile_to_user_sets_flag(self):
        self.client.login(username="stranger@example.com", password="pass123")

        FriendshipRequest.objects.create(
            created_by=self.author_profile,
            created_for=self.stranger_profile,
            status='rejected'
        )

        url = reverse("social_posts:post_list_profile", args=[self.author_profile.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        posts = response.json()["results"]["posts"]
        bodies = [p["body"] for p in posts]

        self.assertIn("Public", bodies)
        self.assertNotIn("Private", bodies)
        self.assertEqual(response.json()["results"]["can_send_friendship_request"], "rejected")


@override_settings(MEDIA_ROOT=os.path.join(tempfile.gettempdir(), "test_media"))
class PostCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_active_user(
            email="user@example.com",
            username="user",
            password="pass123",
            first_name="Test",
            last_name="User",
        )
        self.profile = Profile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

        self.image = create_test_image("test-image.png")
        self.media_path = os.path.join(settings.MEDIA_ROOT, "social/posts")

    def tearDown(self):
        if os.path.exists(self.media_path):
            for f in os.listdir(self.media_path):
                os.remove(os.path.join(self.media_path, f))
            os.rmdir(self.media_path)

    def test_create_post_with_image(self):
        url = reverse("social_posts:post_create")
        data = {
            "body": "New post",
            "is_private": False,
            "images[0]": self.image
        }

        response = self.client.post(url, data=data, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(PostAttachment.objects.count(), 1)

        post = Post.objects.first()
        self.assertEqual(post.body, "New post")
        self.assertEqual(post.created_by, self.profile)
        self.assertEqual(post.attachments.count(), 1)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.posts_count, 1)

    def test_create_post_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)

        url = reverse("social_posts:post_create")
        data = {
            "body": "Test post",
            "is_private": False,
        }

        response = self.client.post(url, data=data, format="multipart")

        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Authentication required")
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_with_invalid_body_returns_400(self):
        url = reverse("social_posts:post_create")
        data = {
            "body": "s",
            "is_private": False
        }

        response = self.client.post(url, data=data, format="multipart")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Form is not valid")
        self.assertEqual(Post.objects.count(), 0)


class SearchApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = create_active_user(
            email='test@example.com',
            username='testuser',
            password='pass123',
            first_name='John',
            last_name='Doe'
        )
        self.profile = Profile.objects.create(user=self.user)
        self.client.force_authenticate(self.user)

        self.friend = create_active_user(
            email='friend@example.com',
            username='frienduser',
            password='pass123',
            first_name='Jane',
            last_name='Smith'
        )
        self.friend_profile = Profile.objects.create(user=self.friend)
        self.profile.friends.add(self.friend_profile)

        self.public_post = Post.objects.create(
            body='This is a public post about Django',
            is_private=False,
            created_by=self.friend_profile
        )
        self.private_post = Post.objects.create(
            body='Secret post from friend',
            is_private=True,
            created_by=self.friend_profile
        )
        self.own_post = Post.objects.create(
            body='My own private Django post',
            is_private=True,
            created_by=self.profile
        )

    def test_search_profiles_get(self):
        url = reverse("social_posts:search") + "?query=Jane"
        response = self.client.get(url)
        results = response.data["results"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results['profiles']), 1)
        self.assertEqual(results['profiles'][0]['first_name'], 'Jane')

    def test_search_profiles_post(self):
        url = reverse("social_posts:search")
        response = self.client.post(url, {"query": "Jane"}, format="json")
        results = response.data["results"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results['profiles']), 1)

    def test_search_posts_public_and_friends(self):
        url = reverse("social_posts:search") + "?query=Django"
        response = self.client.get(url)
        results = response.data["results"]
        post_bodies = [p["body"] for p in results["posts"]]
        self.assertIn(self.public_post.body, post_bodies)
        self.assertIn(self.own_post.body, post_bodies)
        self.assertNotIn(self.private_post.body, post_bodies)

    def test_search_returns_empty(self):
        url = reverse("social_posts:search") + "?query=NothingMatches"
        response = self.client.get(url)
        results = response.data["results"]
        self.assertEqual(len(results['profiles']), 0)
        self.assertEqual(len(results['posts']), 0)

    def test_search_pagination(self):
        for i in range(10):
            Post.objects.create(body=f"Post {i} Django", is_private=False, created_by=self.friend_profile)

        url = reverse("social_posts:search") + "?query=Django&page_size=5"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertLessEqual(len(response.data["results"]["posts"]), 5)


class PostLikeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.author_user = create_active_user(username="author",
                                              email="author@example.com",
                                              password="pass123",
                                              first_name="Test_author",
                                              last_name="User_author")
        self.liker_user = create_active_user(username="liker",
                                             email="liker@example.com",
                                             password="pass123",
                                             first_name="Test_liker",
                                             last_name="User_liker")

        self.author_profile = Profile.objects.create(user=self.author_user)
        self.liker_profile = Profile.objects.create(user=self.liker_user)

        self.post = Post.objects.create(
            body="Test Post", created_by=self.author_profile, is_private=False
        )

        self.like_url = reverse("social_posts:post_like", kwargs={"pk": self.post.pk})

    def test_authenticated_user_can_like_post(self):
        self.client.force_authenticate(user=self.liker_user)

        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "like created")
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.post.likes.count(), 1)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes_count, 1)

    def test_user_cannot_like_twice(self):
        self.client.force_authenticate(user=self.liker_user)

        self.client.post(self.like_url)
        response = self.client.post(self.like_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "post already liked")
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.post.likes.count(), 1)

    def test_unauthenticated_user_cannot_like(self):
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Like.objects.count(), 0)

    def test_user_likes_own_post_creates_like_but_no_error(self):
        self.client.force_authenticate(user=self.author_user)

        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "like created")
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.post.likes.count(), 1)


class PostCreateCommentViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = create_active_user(
            email="user@example.com",
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        self.profile = Profile.objects.create(user=self.user)

        self.post = Post.objects.create(
            body="Test post",
            created_by=self.profile,
            is_private=False,
        )
        self.url = reverse("social_posts:post_create_comment", kwargs={"pk": self.post.pk})

    def test_authenticated_user_can_create_comment(self):
        self.client.force_authenticate(user=self.user)
        data = {"body": "Nice post!"}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.body, "Nice post!")
        self.assertEqual(comment.created_by, self.profile)
        self.post.refresh_from_db()
        self.assertEqual(self.post.comments_count, 1)

    def test_unauthenticated_user_cannot_create_comment(self):
        data = {"body": "Anonymous comment"}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Comment.objects.count(), 0)

    def test_empty_comment_body_is_allowed(self):
        self.client.force_authenticate(user=self.user)
        data = {"body": ""}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.body, "")


class GetTrendsViewTest(TestCase):
    def setUp(self):
        self.url = reverse('social_posts:get_trends')

    def test_returns_all_trends(self):
        Trend.objects.create(hashtag="#fitness", occurences=10)
        Trend.objects.create(hashtag="#health", occurences=5)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        hashtags = [t["hashtag"] for t in response.json()]
        self.assertIn("#fitness", hashtags)
        self.assertIn("#health", hashtags)

    def test_returns_empty_list_if_no_trends(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


@override_settings(MEDIA_ROOT=os.path.join(tempfile.gettempdir(), "media"))
class PostDeleteViewTest(TestCase):

    def setUp(self):
        self.user = create_active_user(
            email="user@example.com",
            username="testuser",
            password="123456",
            first_name="Test",
            last_name="User"
        )
        self.client.login(email="user@example.com", password="123456")
        self.profile = Profile.objects.create(user=self.user)

        self.image = create_test_image("test-image.jpg")

        self.attachment = PostAttachment.objects.create(
            image=self.image,
            created_by=self.profile
        )
        self.post = Post.objects.create(
            body="Test post",
            created_by=self.profile
        )

        self.profile.posts_count = 1
        self.profile.save()

        self.post.attachments.add(self.attachment)
        self.post.save()

        self.url = reverse("social_posts:post_delete", kwargs={"pk": self.post.id})

    def tearDown(self):
        media_root = settings.MEDIA_ROOT
        if os.path.exists(media_root):
            for root, dirs, files in os.walk(media_root, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(media_root)

    def test_authenticated_user_can_delete_own_post(self):
        initial_posts_count = self.profile.posts.count()

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "post deleted"})
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(PostAttachment.objects.count(), 0)

        self.assertFalse(os.path.isfile(self.attachment.image.path))

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.posts_count, initial_posts_count - 1)

    def test_unauthenticated_user_cannot_delete_post(self):
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)

    def test_user_cannot_delete_someone_elses_post(self):
        other_user = create_active_user(
            email="other@example.com",
            username="otheruser",
            password="123456",
            first_name="otherTest",
            last_name="otherUser"
        )
        Profile.objects.create(user=other_user)

        self.client.logout()
        self.client.force_login(other_user)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 404)


class PostReportViewTest(TestCase):
    def setUp(self):
        self.user = create_active_user(
            email="user@example.com",
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        self.profile = Profile.objects.create(user=self.user)

        self.client.force_login(self.user)

        self.post = Post.objects.create(
            body="Test post",
            created_by=self.profile
        )

        self.url = reverse("social_posts:post_report", kwargs={"pk": self.post.pk})

    def test_authenticated_user_can_report_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "post reported"})
        self.assertIn(self.profile, self.post.reported_by_users.all())

    def test_unauthenticated_user_cannot_report_post(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)

    def test_multiple_reports_by_same_user_dont_duplicate(self):
        self.client.post(self.url)
        self.client.post(self.url)

        self.post.refresh_from_db()

        self.assertEqual(self.post.reported_by_users.filter(pk=self.profile.pk).count(), 1)
