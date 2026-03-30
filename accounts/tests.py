from django.test import TestCase
from django.contrib.auth import get_user_model


class AccountsTests(TestCase):
    def test_create_user_and_superuser(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@test.com', password='userpass', username='normal')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        superuser = User.objects.create_superuser(email='admin2@test.com', password='adminpass', username='admin2')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

