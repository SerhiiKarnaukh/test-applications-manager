from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, AsyncMock
from rest_framework.test import APIClient
from accounts.models import Account
from social_profiles.models import Profile
from social_chat.models import Conversation, ConversationMessage


def create_active_user(**kwargs):
    user = Account.objects.create_user(**kwargs)
    user.is_active = True
    user.save()
    return user


class ConversationListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user1 = create_active_user(
            email="activate1@example.com",
            username="activator1",
            password="Activate123",
            first_name="Activate1",
            last_name="User1"
        )
        self.user2 = create_active_user(
            email="activate2@example.com",
            username="activator2",
            password="Activate123",
            first_name="Activate2",
            last_name="User2"
        )
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

        self.conv1 = Conversation.objects.create()
        self.conv1.users.add(self.profile1)

        self.conv2 = Conversation.objects.create()
        self.conv2.users.add(self.profile2)

        self.conv3 = Conversation.objects.create()
        self.conv3.users.add(self.profile1, self.profile2)

    def test_authenticated_user_sees_own_conversations(self):
        self.client.login(username="activate1@example.com", password="Activate123")
        response = self.client.get(reverse("conversation_list"))

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)
        conversation_ids = [str(self.conv1.id), str(self.conv3.id)]

        returned_ids = [item["id"] for item in data]
        for expected_id in conversation_ids:
            self.assertIn(expected_id, returned_ids)

        self.assertNotIn(str(self.conv2.id), returned_ids)


class ConversationDetailViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user1 = create_active_user(
            email="test1@example.com",
            username="user1",
            password="pass123",
            first_name="Test1",
            last_name="User1"
        )
        self.user2 = create_active_user(
            email="test2@example.com",
            username="user2",
            password="pass123",
            first_name="Test2",
            last_name="User2"
        )
        self.user2.is_active = True
        self.user2.save()

        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.profile1, self.profile2)

        self.message = ConversationMessage.objects.create(
            conversation=self.conversation,
            body="Hello!",
            sent_to=self.profile2,
            created_by=self.profile1
        )

    def test_user_can_view_conversation_detail(self):
        self.client.login(username="test1@example.com", password="pass123")

        response = self.client.get(reverse("conversation_detail", args=[self.conversation.pk]))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["id"], str(self.conversation.pk))
        self.assertEqual(len(data["messages"]), 1)
        self.assertEqual(data["messages"][0]["body"], "Hello!")

    def test_user_not_in_conversation_gets_404(self):
        outsider = create_active_user(
            email="outsider@example.com",
            username="outsider",
            password="outpass",
            first_name="Out",
            last_name="Sider",
        )
        Profile.objects.create(user=outsider)
        self.client.login(username="outsider@example.com", password="outpass")

        response = self.client.get(reverse("conversation_detail", args=[self.conversation.pk]))
        self.assertEqual(response.status_code, 404)


class ConversationGetOrCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = create_active_user(
            email="user1@example.com",
            username="user1",
            password="pass123",
            first_name="User",
            last_name="One"
        )
        self.user2 = create_active_user(
            email="user2@example.com",
            username="user2",
            password="pass123",
            first_name="User",
            last_name="Two"
        )

        self.profile1 = Profile.objects.create(
            user=self.user1,
            first_name="User",
            last_name="One"
        )
        self.profile2 = Profile.objects.create(
            user=self.user2,
            first_name="User",
            last_name="Two"
        )

        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.profile1, self.profile2)

    def test_returns_existing_conversation(self):
        self.client.login(username="user1@example.com", password="pass123")
        response = self.client.get(reverse("conversation_get_or_create", args=[self.profile2.slug]))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["id"], str(self.conversation.id))
        self.assertEqual(len(data["users"]), 2)

    def test_creates_new_conversation_if_not_exists(self):
        user3 = create_active_user(
            email="user3@example.com",
            username="user3",
            password="pass123",
            first_name="User",
            last_name="Three"
        )
        profile3 = Profile.objects.create(user=user3, first_name="User", last_name="Three")

        self.client.login(username="user1@example.com", password="pass123")
        response = self.client.get(reverse("conversation_get_or_create", args=[profile3.slug]))

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertNotEqual(data["id"], str(self.conversation.id))  # новая беседа
        self.assertEqual(len(data["users"]), 2)

    def test_invalid_slug_returns_404(self):
        self.client.login(username="user1@example.com", password="pass123")
        response = self.client.get(reverse("conversation_get_or_create", args=["nosuchslug"]))
        self.assertEqual(response.status_code, 404)


class ConversationSendMessageViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = create_active_user(
            email="user1@example.com",
            username="user1",
            password="pass123",
            first_name="User",
            last_name="One"
        )
        self.user2 = create_active_user(
            email="user2@example.com",
            username="user2",
            password="pass123",
            first_name="User",
            last_name="Two"
        )

        self.profile1 = Profile.objects.create(user=self.user1, first_name="User", last_name="One")
        self.profile2 = Profile.objects.create(user=self.user2, first_name="User", last_name="Two")

        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.profile1, self.profile2)

    @patch("social_chat.api.create_notification")
    @patch("social_chat.api.get_channel_layer")
    def test_user_can_send_message(self, mock_get_channel_layer, mock_create_notification):
        self.client.login(username="user1@example.com", password="pass123")

        # Asynchronous WebSocket Mock
        mock_group_send = AsyncMock()
        mock_get_channel_layer.return_value.group_send = mock_group_send

        url = reverse("conversation_send_message", args=[self.conversation.pk])
        data = {"body": "Hello, how are you?"}
        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, 200)
        message_data = response.json()

        # Checking response content
        self.assertEqual(message_data["body"], data["body"])
        self.assertEqual(message_data["created_by"]["username"], self.profile1.username)
        self.assertEqual(message_data["sent_to"]["username"], self.profile2.username)

        # Checking that the object is actually created in the database
        self.assertEqual(ConversationMessage.objects.count(), 1)
        msg = ConversationMessage.objects.first()
        self.assertEqual(msg.conversation, self.conversation)
        self.assertEqual(msg.created_by, self.profile1)
        self.assertEqual(msg.sent_to, self.profile2)
        self.assertEqual(msg.body, data["body"])

        # Checking that create_notification is called with the correct arguments
        mock_create_notification.assert_called_once()
        args, kwargs = mock_create_notification.call_args
        self.assertEqual(args[1], "chat_message")
        self.assertEqual(kwargs, {"conversation_message_id": msg.id})

        # Testing WebSocket call
        mock_group_send.assert_awaited_once()
