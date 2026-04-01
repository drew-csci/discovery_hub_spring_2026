import sys
import os

# Add the workspace root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from django.test import TestCase, Client
from django.urls import reverse
from f25_discovery.accounts.models import User, CompanyProfile


class DiscoveryWorkflowTest(TestCase):
    """Comprehensive test for discovery workflow"""
    
    def setUp(self):
        """Set up test users and company profiles"""
        # Create investor user
        self.investor = User.objects.create_user(
            email='investor@test.com',
            username='investor@test.com',
            password='testpass123',
            user_type='investor'
        )
        
        # Create company seeking funding
        self.company1 = User.objects.create_user(
            email='company1@test.com',
            username='company1@test.com',
            password='testpass123',
            user_type='company'
        )
        self.company_profile1 = CompanyProfile.objects.create(
            user=self.company1,
            company_name='TechStartup Inc',
            industry='Software',
            patent_count=50,
            stage='experienced',
            seeking_funding=True,
            description='We build AI solutions'
        )
        
        # Create company NOT seeking funding
        self.company2 = User.objects.create_user(
            email='company2@test.com',
            username='company2@test.com',
            password='testpass123',
            user_type='company'
        )
        self.company_profile2 = CompanyProfile.objects.create(
            user=self.company2,
            company_name='EstablishedCorp',
            industry='Biotech',
            patent_count=20,
            stage='experienced',
            seeking_funding=False,
            description='We are profitable'
        )
        
        self.client = Client()
    
    def test_complete_discovery_workflow(self):
        """Test complete discovery workflow for investor"""
        # Test 1: Unauthenticated user cannot access discovery list
        response = self.client.get(reverse('discovery_list'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        
        # Test 2: Login as investor
        login_success = self.client.login(
            username='investor@test.com',
            password='testpass123'
        )
        self.assertTrue(login_success)
        
        # Test 3: Investor can see discovery list with only companies seeking funding
        response = self.client.get(reverse('discovery_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TechStartup Inc')
        self.assertNotContains(response, 'EstablishedCorp')
        
        # Test 4: Company profile displays all information
        response = self.client.get(
            reverse('company_detail', args=[self.company_profile1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TechStartup Inc')
        self.assertContains(response, 'Software')
        self.assertContains(response, '50')  # patent count