from django.test import TestCase
from accounts.serializers import ProfileCreateSerializer
from accounts.models import Account


class ProfileCreateSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "StrongPass123",
            "first_name": "New",
            "last_name": "User"
        }

    def test_serializer_creates_user_successfully(self):
        serializer = ProfileCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertEqual(user.email, self.valid_data["email"])
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertEqual(user.first_name, self.valid_data["first_name"])
        self.assertEqual(user.last_name, self.valid_data["last_name"])
        self.assertTrue(user.check_password(self.valid_data["password"]))
        self.assertTrue(Account.objects.filter(email=user.email).exists())

    def test_missing_required_fields_fails_validation(self):
        invalid_data = {
            "email": "",
            "username": "",
            "password": "",
            "first_name": "",
            "last_name": ""
        }
        serializer = ProfileCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("username", serializer.errors)
        self.assertIn("password", serializer.errors)
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)

    def test_password_is_hashed(self):
        serializer = ProfileCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertNotEqual(user.password, self.valid_data["password"])
        self.assertTrue(user.check_password(self.valid_data["password"]))
