from django.test import TestCase
from accounts.models import Account


class MyAccountManagerTest(TestCase):

    def test_create_user_successfully(self):
        user = Account.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="SuperSecret123",
            first_name="Test",
            last_name="User"
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("SuperSecret123"))
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superadmin)
        self.assertFalse(user.is_active)

    def test_create_user_missing_email_raises_error(self):
        with self.assertRaisesMessage(ValueError, "User must have an email address"):
            Account.objects.create_user(
                email="",
                username="testuser",
                password="pass",
                first_name="Test",
                last_name="User"
            )

    def test_create_user_missing_username_raises_error(self):
        with self.assertRaisesMessage(ValueError, "User must have an username"):
            Account.objects.create_user(
                email="test@example.com",
                username="",
                password="pass",
                first_name="Test",
                last_name="User"
            )

    def test_create_superuser_successfully(self):
        admin = Account.objects.create_superuser(
            email="admin@example.com",
            username="adminuser",
            password="AdminPass123",
            first_name="Admin",
            last_name="Boss"
        )

        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superadmin)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.check_password("AdminPass123"))

    def test_generate_unique_username_adds_suffix_if_exists(self):
        base_username = "john"
        Account.objects.create_user(
            email="john@example.com",
            username=base_username,
            password="123",
            first_name="John",
            last_name="Doe"
        )

        new_user = Account.objects.create_user(
            email="john2@example.com",
            username=base_username,
            password="456",
            first_name="John",
            last_name="Smith"
        )

        self.assertNotEqual(new_user.username, base_username)
        self.assertTrue(new_user.username.startswith("john_"))


class AccountModelMethodTest(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="Secret123!",
            first_name="Test",
            last_name="User"
        )

    def test_full_name_returns_correct_string(self):
        self.assertEqual(self.user.full_name(), "Test User")

    def test_str_returns_email(self):
        self.assertEqual(str(self.user), "testuser@example.com")

    def test_has_perm_returns_is_admin_true(self):
        self.user.is_admin = True
        self.assertTrue(self.user.has_perm("any_perm"))

    def test_has_perm_returns_is_admin_false(self):
        self.user.is_admin = False
        self.assertFalse(self.user.has_perm("any_perm"))

    def test_has_module_perms_always_true(self):
        self.assertTrue(self.user.has_module_perms("any_module"))
