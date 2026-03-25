from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import ProfileUpdateForm
import datetime

User = get_user_model()

class UserModelTest(TestCase):
    def test_user_creation_with_new_fields(self):
        """Test that a user can be created with the new fields"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            phone_number='+1234567890',
            birthday='1990-01-01',
            country='USA',
            state='California',
            city='San Francisco'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertEqual(str(user.birthday), '1990-01-01')
        self.assertEqual(user.country, 'USA')
        self.assertEqual(user.state, 'California')
        self.assertEqual(user.city, 'San Francisco')

    def test_user_display_name(self):
        """Test the display_name property"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.display_name, 'John Doe')

        # Test with no name
        user2 = User.objects.create_user(
            email='test2@example.com',
            password='testpass123'
        )
        self.assertEqual(user2.display_name, 'test2@example.com')

class ProfileUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_form_includes_new_fields(self):
        """Test that the form includes all the new fields"""
        form = ProfileUpdateForm(instance=self.user)
        expected_fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'state', 'city', 'birth_month', 'birth_day', 'birth_year']
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_form_validation_with_birthday(self):
        """Test form validation with birthday dropdowns"""
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'phone_number': '+1987654321',
            'birth_month': '5',
            'birth_day': '15',
            'birth_year': '1990',
            'country': 'United States',
            'state': 'California',
            'city': 'Los Angeles'
        }
        form = ProfileUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['birthday'], datetime.date(1990, 5, 15))

    def test_birthday_validation_partial(self):
        """Test that partial birthday data is rejected"""
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'birth_month': '5',
            'birth_day': '',  # Missing day
            'birth_year': '1990',
        }
        form = ProfileUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)  # Non-field error

    def test_email_uniqueness(self):
        """Test that email must be unique"""
        # Create another user
        User.objects.create_user(email='existing@example.com', password='testpass123')

        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'existing@example.com',  # This email already exists
            'phone_number': '+1987654321',
            'birth_month': '5',
            'birth_day': '15',
            'birth_year': '1990',
            'country': 'United States',
            'state': 'California',
            'city': 'Los Angeles'
        }
        form = ProfileUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
