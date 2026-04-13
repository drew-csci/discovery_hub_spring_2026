from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from .models import InventionDisclosure, Opportunity


class OpportunitySearchUnitTests(TestCase):
    """Unit tests for opportunity search filtering logic"""

    def setUp(self):
        """Create test opportunities"""
        Opportunity.objects.create(
            name="Software Engineer",
            type="Job",
            category="Technology",
            description="Build amazing products"
        )
        Opportunity.objects.create(
            name="Data Science Internship",
            type="Internship",
            category="Technology",
            description="Analyze data and trends"
        )
        Opportunity.objects.create(
            name="Marketing Grant",
            type="Grant",
            category="Business",
            description="Fund marketing initiatives"
        )
        Opportunity.objects.create(
            name="Science Fellowship",
            type="Fellowship",
            category="Science",
            description="Support science research"
        )

    def test_opportunity_search_by_keyword_match(self):
        """Unit Test: Search with valid keyword returns matching opportunities"""
        opportunities = Opportunity.objects.filter(name__icontains="Engineer")
        self.assertEqual(opportunities.count(), 1)
        self.assertEqual(opportunities[0].name, "Software Engineer")

    def test_opportunity_search_by_keyword_no_match(self):
        """Unit Test: Search with non-matching keyword returns empty"""
        opportunities = Opportunity.objects.filter(name__icontains="NonExistent")
        self.assertEqual(opportunities.count(), 0)

    def test_opportunity_search_by_type_filter(self):
        """Unit Test: Filter by type returns matching opportunities"""
        opportunities = Opportunity.objects.filter(type__iexact="Job")
        self.assertEqual(opportunities.count(), 1)
        self.assertEqual(opportunities[0].type, "Job")

    def test_opportunity_search_by_category_filter(self):
        """Unit Test: Filter by category returns matching opportunities"""
        opportunities = Opportunity.objects.filter(category__iexact="Technology")
        self.assertEqual(opportunities.count(), 2)

    def test_opportunity_search_combined_filters(self):
        """Unit Test: Combine keyword and category filters"""
        opportunities = Opportunity.objects.filter(
            name__icontains="Science"
        ).filter(category__iexact="Science")
        self.assertEqual(opportunities.count(), 1)
        self.assertEqual(opportunities[0].name, "Science Fellowship")

    def test_opportunity_search_empty_result(self):
        """Unit Test: Edge case - search matching no opportunities"""
        opportunities = Opportunity.objects.filter(
            type__iexact="Unknown"
        )
        self.assertEqual(opportunities.count(), 0)

    def test_opportunity_search_happy_path_valid_keyword(self):
        """Unit Test: Happy path - valid keyword returns expected opportunity"""
        opportunities = Opportunity.objects.filter(name__icontains="Engineer")
        assert opportunities.count() == 1
        assert opportunities[0].name == "Software Engineer"
        assert opportunities[0].type == "Job"

    def test_opportunity_search_edge_case_empty_keyword(self):
        """Unit Test: Edge case - empty keyword returns all opportunities"""
        opportunities = Opportunity.objects.all()
        assert opportunities.count() == 4  # All created in setUp

    def test_opportunity_str_happy_path_returns_name(self):
        """Unit Test: Happy path - __str__ returns the opportunity name"""
        opp = Opportunity.objects.create(
            name="UX Researcher",
            type="Job",
            category="Design",
            description="User research work"
        )
        self.assertEqual(str(opp), "UX Researcher")

    def test_opportunity_str_edge_case_empty_name_returns_empty_string(self):
        """Unit Test: Edge case - __str__ handles empty/missing name gracefully"""
        opp = Opportunity.objects.create(
            name="",
            type="Job",
            category="Design",
            description="No name"
        )
        self.assertEqual(str(opp), "")


class OpportunitySearchIntegrationTests(TestCase):
    """Integration tests for the full search view workflow"""

    def setUp(self):
        """Create test client and opportunities"""
        self.client = Client()
        Opportunity.objects.create(
            name="Python Developer",
            type="Job",
            category="Technology",
            description="Looking for Python expertise"
        )
        Opportunity.objects.create(
            name="Java Developer",
            type="Job",
            category="Technology",
            description="Build Java applications"
        )
        Opportunity.objects.create(
            name="Design Scholarship",
            type="Scholarship",
            category="Education",
            description="Support design students"
        )

    def test_search_view_returns_200_ok(self):
        """Integration Test: Search page loads successfully"""
        response = self.client.get(reverse('opportunity_search'))
        self.assertEqual(response.status_code, 200)

    def test_search_view_renders_search_template(self):
        """Integration Test: Search view uses correct template"""
        response = self.client.get(reverse('opportunity_search'))
        self.assertTemplateUsed(response, 'pages/search.html')

    def test_search_view_with_keyword_query(self):
        """Integration Test: Search form with keyword filters results"""
        response = self.client.get(
            reverse('opportunity_search'),
            {'q': 'Python'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Developer")
        self.assertNotContains(response, "Java Developer")

    def test_search_view_with_type_filter(self):
        """Integration Test: Type filter narrows results"""
        response = self.client.get(
            reverse('opportunity_search'),
            {'type': 'Scholarship'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Design Scholarship")
        self.assertNotContains(response, "Python Developer")

    def test_search_view_with_category_filter(self):
        """Integration Test: Category filter works end-to-end"""
        response = self.client.get(
            reverse('opportunity_search'),
            {'category': 'Technology'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Developer")
        self.assertContains(response, "Java Developer")
        self.assertNotContains(response, "Design Scholarship")

    def test_search_view_combined_filters(self):
        """Integration Test: Query + type + category filters together"""
        response = self.client.get(
            reverse('opportunity_search'),
            {'q': 'Developer', 'type': 'Job', 'category': 'Technology'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Developer")
        self.assertContains(response, "Java Developer")

    def test_search_view_no_results_message(self):
        """Integration Test: No results displays helpful message"""
        response = self.client.get(
            reverse('opportunity_search'),
            {'q': 'NonExistentQuery'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results found")

    def test_search_view_empty_query_shows_all(self):
        """Integration Test: Empty search query returns all opportunities"""
        response = self.client.get(reverse('opportunity_search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Developer")
        self.assertContains(response, "Java Developer")
        self.assertContains(response, "Design Scholarship")

    def test_search_view_pagination(self):
        """Integration Test: Pagination works with per_page parameter"""
        response = self.client.get(
            reverse('opportunity_search'),
            {'per_page': 2, 'page': 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('opportunities' in response.context)

    def test_search_view_context_contains_query_params(self):
        """Integration Test: Template context includes search parameters"""
        response = self.client.get(
            reverse('opportunity_search'),
            {'q': 'test', 'type': 'Job', 'category': 'Tech'}
        )
        self.assertEqual(response.context['query'], 'test')
        self.assertEqual(response.context['type'], 'Job')
        self.assertEqual(response.context['category'], 'Tech')

    def test_search_view_load_time_displayed(self):
        """Integration Test: Load time is calculated and shown"""
        response = self.client.get(reverse('opportunity_search'))
        self.assertIn('load_time', response.context)
        self.assertTrue(
            isinstance(response.context['load_time'], str),
            "load_time should be a string"
        )

    def test_search_workflow_with_query_and_filters(self):
        """Integration Test: search endpoint + DB filters compose correctly"""
        # This setUp created Python Developer, Java Developer, Design Scholarship
        response = self.client.get(
            reverse('opportunity_search'),
            {'q': 'Developer', 'type': 'Job', 'category': 'Technology'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Developer")
        self.assertContains(response, "Java Developer")
        self.assertNotContains(response, "Design Scholarship")
        self.assertEqual(response.context['query'], 'Developer')
        self.assertEqual(response.context['type'], 'Job')
        self.assertEqual(response.context['category'], 'Technology')


class InventionDisclosureFormTests(TestCase):
    def test_required_fields_enforced(self):
        response = self.client.post(reverse('submit_disclosure'), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inventor name is required')
        self.assertContains(response, 'Email address is required')
        self.assertContains(response, 'Invention title is required')
        self.assertContains(response, 'Description is required')

    def test_invalid_email_shows_inline_error(self):
        response = self.client.post(reverse('submit_disclosure'), {
            'inventor_name': 'Jane Doe',
            'inventor_email': 'invalid-email',
            'invention_title': 'Test Invention',
            'invention_description': 'A useful invention',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address')

    def test_successful_submission_sends_confirmation_email(self):
        mail.outbox = []
        response = self.client.post(reverse('submit_disclosure'), {
            'inventor_name': 'Jane Doe',
            'inventor_email': 'jane@example.com',
            'invention_title': 'Test Invention',
            'invention_description': 'A useful invention description that is long enough.',
            'technology_field': 'AI',
            'date_of_invention': '2025-01-01',
        }, follow=True)
        self.assertEqual(InventionDisclosure.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(response, 'Disclosure Submitted')
        email = mail.outbox[0]
        self.assertEqual(email.to, ['jane@example.com'])
        self.assertIn('Invention disclosure submitted: Test Invention', email.subject)
        self.assertIn('If this was you, no action is needed.', email.body)
        self.assertIn('If this was NOT you, please contact our support team immediately.', email.body)
        self.assertIn('support@discovery-hub.edu', email.body)
