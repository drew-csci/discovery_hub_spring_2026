from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class UserModelTests(TestCase):
    def test_save_sets_username_to_email_when_missing(self):
        user = User(email='no_username@example.com', username='')
        user.set_password('SomePass123!')
        user.save()
        self.assertEqual(user.username, 'no_username@example.com')

    def test_display_name_prefers_full_name(self):
        user = User.objects.create_user(
            email='full_name@example.com',
            username='full_name@example.com',
            password='SomePass123!',
            first_name='Ada',
            last_name='Lovelace',
        )
        self.assertEqual(user.display_name, 'Ada Lovelace')

    def test_display_name_falls_back_to_email(self):
        user = User.objects.create_user(
            email='fallback@example.com',
            username='fallback@example.com',
            password='SomePass123!',
            first_name='',
            last_name='',
        )
        self.assertEqual(user.display_name, 'fallback@example.com')


class RegisterViewTests(TestCase):
    def test_register_get_prefills_user_type_from_querystring(self):
        response = self.client.get(reverse('register') + '?type=company')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial.get('user_type'), 'company')

    def test_register_get_prefills_user_type_from_session_regression(self):
        """Regression test: if user_type is stored in session, it should prefill register."""
        self.client.get(reverse('login') + '?type=investor')  # sets session['selected_user_type']

        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial.get('user_type'), 'investor')

    def test_register_post_creates_user_and_logs_in(self):
        payload = {
            'email': 'new_user@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 'investor',
        }
        response = self.client.post(reverse('register'), payload, follow=True)

        self.assertTrue(User.objects.filter(email='new_user@example.com').exists())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.email, 'new_user@example.com')

    def test_register_rejects_missing_email_negative(self):
        payload = {
            'email': '',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 'company',
        }
        response = self.client.post(reverse('register'), payload)
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertTrue(form.errors.get('email'))
        self.assertFalse(User.objects.filter(email='').exists())

    def test_register_rejects_invalid_email_negative(self):
        payload = {
            'email': 'not-an-email',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 'company',
        }
        response = self.client.post(reverse('register'), payload)
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertIn('Enter a valid email address.', form.errors.get('email', []))

    def test_register_rejects_password_mismatch_negative(self):
        payload = {
            'email': 'mismatch@example.com',
            'password1': 'StrongPass123!',
            'password2': 'DifferentPass123!',
            'user_type': 'company',
        }
        response = self.client.post(reverse('register'), payload)
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)
        # Message is from Django's UserCreationForm; match loosely to avoid locale/punctuation issues.
        self.assertTrue(any('match' in e.lower() for e in form.errors.get('password2', [])))
        self.assertFalse(User.objects.filter(email='mismatch@example.com').exists())


class CustomLoginViewTests(TestCase):
    def setUp(self):
        self.password = 'SomePass123!'
        self.user = User.objects.create_user(
            email='login_user@example.com',
            username='login_user@example.com',
            password=self.password,
            user_type='university',
        )

    def test_login_get_type_sets_session_and_context(self):
        response = self.client.get(reverse('login') + '?type=investor')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_user_type'], 'investor')

        session = self.client.session
        self.assertEqual(session.get('selected_user_type'), 'investor')

    def test_login_post_authenticates_with_email_in_username_field(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.user.email, 'password': self.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.email, self.user.email)

    def test_login_rejects_wrong_password_negative(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.user.email, 'password': 'WrongPass123!'},
        )
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)
        # AuthenticationForm typically attaches invalid login to __all__.
        self.assertTrue(form.errors)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class ProfileUpdateViewTests(TestCase):
    def setUp(self):
        self.user_password = 'SomePass123!'
        self.user = User.objects.create_user(
            email='profile_user@example.com',
            username='profile_user@example.com',
            password=self.user_password,
            user_type='company',
        )
        self.other_user = User.objects.create_user(
            email='already_taken@example.com',
            username='already_taken@example.com',
            password='OtherPass123!',
        )

    def test_settings_requires_login(self):
        response = self.client.get(reverse('account_settings'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_settings_rejects_duplicate_email(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('account_settings'),
            {
                'first_name': 'New',
                'last_name': 'Name',
                'email': self.other_user.email,  # should fail clean_email
            },
        )

        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertIn('This email address is already in use.', form.errors.get('email', []))

    def test_settings_rejects_blank_email_negative(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('account_settings'),
            {'first_name': 'A', 'last_name': 'B', 'email': ''},
        )

        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertTrue(form.errors.get('email'))

    def test_settings_updates_profile(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('account_settings'),
            {
                'first_name': 'Grace',
                'last_name': 'Hopper',
                'email': 'profile_user@example.com',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Grace')
        self.assertEqual(self.user.last_name, 'Hopper')
        self.assertEqual(self.user.email, 'profile_user@example.com')


class AccountsIntegrationAndSmokeTests(TestCase):
    def test_smoke_login_and_register_pages_load(self):
        for name in ['login', 'register']:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, f'{name} should return 200')

    def test_login_redirects_when_already_authenticated_regression(self):
        """Regression: redirect_authenticated_user=True should bounce logged-in users."""
        user = User.objects.create_user(
            email='already_auth@example.com',
            username='already_auth@example.com',
            password='SomePass123!',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('screen1'))

    def test_full_user_journey_register_then_update_profile_integration(self):
        """Integration test across accounts + pages: register -> screen1 -> update settings."""
        payload = {
            'email': 'journey@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 'company',
        }
        response = self.client.post(reverse('register'), payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Should land on screen1 and be able to load it.
        response = self.client.get(reverse('screen1'))
        self.assertEqual(response.status_code, 200)

        # Update profile settings.
        response = self.client.post(
            reverse('account_settings'),
            {'first_name': 'Test', 'last_name': 'User', 'email': 'journey@example.com'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        u = User.objects.get(email='journey@example.com')
        self.assertEqual(u.first_name, 'Test')
        self.assertEqual(u.last_name, 'User')
