from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountViewTests(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_creates_user_and_logs_in(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'StrongPassw0rd!',
            'password2': 'StrongPassw0rd!',
            'user_type': User.UserType.COMPANY,
        }

        response = self.client.post(reverse('register'), form_data)

        self.assertRedirects(response, reverse('screen1'))
        user = User.objects.get(email='test@example.com')
        self.assertTrue(user.check_password('StrongPassw0rd!'))
        self.assertEqual(user.user_type, User.UserType.COMPANY)
        self.assertIn('_auth_user_id', self.client.session)

    def test_register_with_mismatched_passwords(self):
        form_data = {
            'email': 'bad@example.com',
            'password1': 'Password123!',
            'password2': 'DifferentPassword!',
            'user_type': User.UserType.COMPANY,
        }
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match.")
        self.assertFalse(User.objects.filter(email='bad@example.com').exists())

    def test_register_with_duplicate_email(self):
        User.objects.create_user(email='duplicate@example.com', username='dup', password='pass')
        form_data = {
            'email': 'duplicate@example.com',
            'password1': 'AnotherPass123!',
            'password2': 'AnotherPass123!',
            'user_type': User.UserType.COMPANY,
        }
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User with this Email already exists.")
        self.assertEqual(User.objects.filter(email='duplicate@example.com').count(), 1)

    def test_login_with_email_redirects_to_screen1(self):
        user = User.objects.create_user(
            email='login@example.com',
            username='login@example.com',
            password='ValidPass123!'
        )

        response = self.client.post(reverse('login'), {
            'username': 'login@example.com',
            'password': 'ValidPass123!',
        })

        self.assertRedirects(response, reverse('screen1'))
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_profile_update_requires_login(self):
        response = self.client.get(reverse('account_settings'))
        login_url = reverse('login')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(login_url))

    def test_profile_update_changes_user_data(self):
        user = User.objects.create_user(
            email='profile@example.com',
            username='profile@example.com',
            password='Password123!'
        )
        self.client.force_login(user)

        response = self.client.post(reverse('account_settings'), {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'profile@example.com',
        })

        self.assertRedirects(response, reverse('account_settings'))
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'profile@example.com')

    def test_registration_performance(self):
        import time
        form_data = {
            'email': 'perf@example.com',
            'password1': 'StrongPassw0rd!',
            'password2': 'StrongPassw0rd!',
            'user_type': User.UserType.COMPANY,
        }
        start = time.perf_counter()
        response = self.client.post(reverse('register'), form_data)
        elapsed = time.perf_counter() - start
        self.assertEqual(response.status_code, 302)
        self.assertLess(elapsed, 0.5, f"Registration took too long: {elapsed:.3f} seconds")

    def test_registration_and_login_integration(self):
        # Register a new user
        reg_data = {
            'email': 'integration@example.com',
            'password1': 'StrongPassw0rd!',
            'password2': 'StrongPassw0rd!',
            'user_type': User.UserType.INVESTOR,
        }
        reg_response = self.client.post(reverse('register'), reg_data)
        self.assertRedirects(reg_response, reverse('screen1'))
        self.assertTrue(User.objects.filter(email='integration@example.com').exists())

        # Log out
        self.client.logout()

        # Log in with the new user
        login_response = self.client.post(reverse('login'), {
            'username': 'integration@example.com',
            'password': 'StrongPassw0rd!',
        })
        self.assertRedirects(login_response, reverse('screen1'))
        self.assertIn('_auth_user_id', self.client.session)


class SmokeTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
