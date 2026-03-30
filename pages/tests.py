from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Company, University, Patent, SystemSetting


class PageModelAndAdminDashboardTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create_superuser(
            email='admin@test.com', password='adminpass', username='admin1'
        )
        self.user = User.objects.create_user(
            email='user@test.com', password='userpass', username='user1', is_staff=False
        )

        self.company = Company.objects.create(name='TestCo', industry='Tech')
        self.university = University.objects.create(name='Test University', country='US')
        self.patent = Patent.objects.create(title='Test Patent', owner_company=self.company, status='filed')
        self.setting = SystemSetting.objects.create(key='maintenance_mode', value='off', is_active=True)

    def test_system_setting_get_value(self):
        self.assertEqual(SystemSetting.get_value('maintenance_mode', default='unknown'), 'off')
        self.assertEqual(SystemSetting.get_value('missing_key', default='unknown'), 'unknown')

    def test_admin_dashboard_requires_superuser(self):
        self.client.login(email='user@test.com', password='userpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_superuser_access(self):
        self.client.login(email='admin@test.com', password='adminpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')
        self.assertContains(response, 'Total users:')
        self.assertContains(response, 'Companies')
        self.assertContains(response, 'Universities')
        self.assertContains(response, 'Patents')

    def test_admin_dashboard_uses_correct_template(self):
        self.client.login(email='admin@test.com', password='adminpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        # Check that the response contains expected content from the dashboard
        self.assertContains(response, 'Admin Dashboard')
        self.assertContains(response, 'Total users:')

    def test_superuser_workflow_protected_admin_dashboard(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'admin@test.com', 'password': 'adminpass'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_superuser)

        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total users:')
        self.assertContains(response, 'Companies')
        self.assertContains(response, 'Universities')
        self.assertContains(response, 'Patents')

    def test_data_models_persistence(self):
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(University.objects.count(), 1)
        self.assertEqual(Patent.objects.filter(status='filed').count(), 1)
        self.assertEqual(SystemSetting.objects.filter(key='maintenance_mode').first().value, 'off')
