from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import Account
from social_profiles.models import Profile
from social_chat.models import Conversation, ConversationMessage


class ConversationListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user1 = Account.objects.create_user(
            email="activate1@example.com",
            username="activator1",
            password="Activate123",
            first_name="Activate1",
            last_name="User1"
        )
        self.user1.is_active = True
        self.user1.save()
        self.user2 = Account.objects.create_user(
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

        self.user1 = Account.objects.create_user(
            email="test1@example.com",
            username="user1",
            password="pass123",
            first_name="Test1",
            last_name="User1"
        )
        self.user1.is_active = True
        self.user1.save()
        self.user2 = Account.objects.create_user(
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
        outsider = Account.objects.create_user(
            email="outsider@example.com",
            username="outsider",
            password="outpass",
            first_name="Out",
            last_name="Sider",
        )
        outsider.is_active = True
        outsider.save()
        Profile.objects.create(user=outsider)
        self.client.login(username="outsider@example.com", password="outpass")

        response = self.client.get(reverse("conversation_detail", args=[self.conversation.pk]))
        self.assertEqual(response.status_code, 404)
