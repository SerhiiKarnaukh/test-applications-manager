from django.test import TestCase
from unittest.mock import patch, AsyncMock
from accounts.models import Account
from social_profiles.models import Profile
from social_notification.utils import send_notification


class SendNotificationTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email="notify@example.com",
            username="notifier",
            password="pass123",
            first_name="Notify",
            last_name="User"
        )
        self.user.is_active = True
        self.user.save()

        self.profile = Profile.objects.create(user=self.user)

    @patch("social_notification.utils.get_channel_layer")
    def test_send_notification_sends_correct_message(self, mock_get_channel_layer):
        mock_group_send = AsyncMock()
        mock_get_channel_layer.return_value.group_send = mock_group_send

        message = "chat_message"
        group_name = f"notifications_{self.profile.id}"

        send_notification(self.profile, message)

        mock_group_send.assert_called_once_with(group_name, {
            "type": "send_notification",
            "message": message
        })
