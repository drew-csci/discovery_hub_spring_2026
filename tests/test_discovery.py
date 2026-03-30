import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'f25_discovery'))

from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, CompanyProfile


class DiscoveryListViewTest(TestCase):
    """Test the discovery list view for investors"""
    
    def setUp(self):
        """Set up test investor and company profiles"""
        # Create investor user
        self.investor = User.objects.create_user(
            email='investor@test.com',
            username='investor_user',
            password='testpass123',
            user_type='investor'
        )
        
        # Create company seeking funding
        self.company1 = User.objects.create_user(
            email='company1@test.com',
            username='company1',
            password='testpass123',
            user_type='company'
        )
        self.company_profile1 = CompanyProfile.objects.create(
            user=self.company1,
            company_name='TechStartup Inc',
            industry='Software',
            patent_count=5,
            company_stage='new',
            seeking_funding=True,
            description='We build AI solutions'
        )
        
        # Create company NOT seeking funding
        self.company2 = User.objects.create_user(
            email='company2@test.com',
            username='company2',
            password='testpass123',
            user_type='company'
        )
        self.company_profile2 = CompanyProfile.objects.create(
            user=self.company2,
            company_name='EstablishedCorp',
            industry='Biotech',
            patent_count=20,
            company_stage='experienced',
            seeking_funding=False,
            description='We are profitable'
        )
        
        self.client = Client()
    
    def test_discovery_list_requires_login(self):
        """Test that discovery list requires login"""
        response = self.client.get(reverse('discovery_list'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
    
    def test_discovery_list_shows_only_seeking_funding(self):
        """Test that only companies seeking funding are displayed"""
        self.client.login(email='investor@test.com', password='testpass123')
        response = self.client.get(reverse('discovery_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TechStartup Inc')
        self.assertNotContains(response, 'EstablishedCorp')
    
    def test_discovery_list_filter_by_industry(self):
        """Test filtering companies by industry"""
        self.client.login(email='investor@test.com', password='testpass123')
        response = self.client.get(reverse('discovery_list') + '?industry=Software')
        self.assertContains(response, 'TechStartup Inc')


class CompanyDetailViewTest(TestCase):
    """Test the company detail view"""
    
    def setUp(self):
        """Set up test investor and company"""
        self.investor = User.objects.create_user(
            email='investor@test.com',
            username='investor_user',
            password='testpass123',
            user_type='investor'
        )
        
        self.company = User.objects.create_user(
            email='company@test.com',
            username='company',
            password='testpass123',
            user_type='company'
        )
        self.company_profile = CompanyProfile.objects.create(
            user=self.company,
            company_name='InnovateTech',
            industry='Software',
            patent_count=10,
            company_stage='new',
            seeking_funding=True,
            description='Building the future'
        )
        
        self.client = Client()
    
    def test_company_detail_page_loads(self):
        """Test that company detail page loads"""
        self.client.login(email='investor@test.com', password='testpass123')
        response = self.client.get(
            reverse('company_detail', args=[self.company_profile.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'InnovateTech')
    
    def test_company_detail_shows_all_info(self):
        """Test that company detail displays all information"""
        self.client.login(email='investor@test.com', password='testpass123')
        response = self.client.get(
            reverse('company_detail', args=[self.company_profile.id])
        )
        self.assertContains(response, 'Software')
        self.assertContains(response, '10')  # patent count
        self.assertContains(response, 'Building the future')


class RiskCalculatorTest(TestCase):
    """Test the risk calculator functionality"""
    
    def setUp(self):
        """Set up test investor and companies"""
        self.investor = User.objects.create_user(
            email='investor@test.com',
            username='investor_user',
            password='testpass123',
            user_type='investor'
        )
        
        self.company = User.objects.create_user(
            email='company@test.com',
            username='company',
            password='testpass123',
            user_type='company'
        )
        
        self.client = Client()
    
    def test_low_risk_calculation(self):
        """Test that established company with patents = Low risk"""
        company_profile = CompanyProfile.objects.create(
            user=self.company,
            company_name='VeteranTech',
            industry='Software',
            patent_count=50,
            company_stage='experienced',
            seeking_funding=True,
            description='Established company'
        )
        
        self.client.login(email='investor@test.com', password='testpass123')
        response = self.client.post(
            reverse('calculate_risk', args=[company_profile.id])
        )
        self.assertContains(response, 'Low')
    
    def test_high_risk_calculation(self):
        """Test that new startup with few patents = High risk"""
        company_profile = CompanyProfile.objects.create(
            user=self.company,
            company_name='StartupRisk',
            industry='Biotech',
            patent_count=1,
            company_stage='new',
            seeking_funding=True,
            description='Brand new startup'
        )
        
        self.client.login(email='investor@test.com', password='testpass123')
        response = self.client.post(
            reverse('calculate_risk', args=[company_profile.id])
        )
        self.assertContains(response, 'High')
    
    def test_medium_risk_calculation(self):
        """Test that mid-range company = Medium risk"""
        company_profile = CompanyProfile.objects.create(
            user=self.company,
            company_name='MidTech',
            industry='Software',
            patent_count=15,
            company_stage='new',
            seeking_funding=True,
            description='Growing startup'
        )
        
        self.client.login(email='investor@test.com', password='testpass123')
        response = self.client.post(
            reverse('calculate_risk', args=[company_profile.id])
        )
        self.assertContains(response, 'Medium')


class UserAccessControlTest(TestCase):
    """Test role-based access control"""
    
    def setUp(self):
        """Set up test users with different roles"""
        self.investor = User.objects.create_user(
            email='investor@test.com',
            username='investor',
            password='testpass123',
            user_type='investor'
        )
        
        self.company = User.objects.create_user(
            email='company@test.com',
            username='company',
            password='testpass123',
            user_type='company'
        )
        
        self.university = User.objects.create_user(
            email='university@test.com',
            username='university',
            password='testpass123',
            user_type='university'
        )
        
        self.client = Client()
    
    def test_only_investor_can_access_discovery(self):
        """Test that only investor users can access discovery"""
        # Company user should not access
        self.client.login(email='company@test.com', password='testpass123')
        response = self.client.get(reverse('discovery_list'))
        self.assertNotEqual(response.status_code, 200)
        
        # University user should not access
        self.client.logout()
        self.client.login(email='university@test.com', password='testpass123')
        response = self.client.get(reverse('discovery_list'))
        self.assertNotEqual(response.status_code, 200)
        
        # Investor should access
        self.client.logout()
        self.client.login(email='investor@test.com', password='testpass123')
        response = self.client.get(reverse('discovery_list'))
        self.assertEqual(response.status_code, 200)


class CompanyProfileModelTest(TestCase):
    """Test CompanyProfile model"""
    
    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            email='company@test.com',
            username='company',
            password='testpass123',
            user_type='company'
        )
    
    def test_company_profile_creation(self):
        """Test that CompanyProfile can be created"""
        profile = CompanyProfile.objects.create(
            user=self.user,
            company_name='TestCorp',
            industry='Software',
            patent_count=5,
            company_stage='new',
            seeking_funding=True
        )
        self.assertEqual(profile.company_name, 'TestCorp')
        self.assertTrue(profile.seeking_funding)
    
    def test_company_profile_str(self):
        """Test that CompanyProfile __str__ returns company name"""
        profile = CompanyProfile.objects.create(
            user=self.user,
            company_name='MyCompany',
            industry='Biotech',
            patent_count=10,
            company_stage='experienced',
            seeking_funding=True
        )
        self.assertEqual(str(profile), 'MyCompany')
    
    def test_company_profile_defaults(self):
        """Test CompanyProfile default values"""
        profile = CompanyProfile.objects.create(
            user=self.user,
            company_name='DefaultCorp',
            industry='Software',
            patent_count=0,
            company_stage='new'
        )
        self.assertTrue(profile.seeking_funding)  # Default should be True