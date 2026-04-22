from django.test import TestCase, Client
from django.urls import reverse
from .models import Opportunity


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


class ScreenViewsAuthAndRoleTests(TestCase):
    def test_screen1_requires_login(self):
        response = self.client.get(reverse('screen1'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_screen1_sets_role_from_user_type(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(
            email='company_user@example.com',
            username='company_user@example.com',
            password='SomePass123!',
            user_type='company',
        )

        self.client.force_login(user)
        response = self.client.get(reverse('screen1'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/screen1.html')
        self.assertEqual(response.context.get('role'), 'Company')

    def test_screen2_sets_role_from_user_type(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(
            email='investor_user@example.com',
            username='investor_user@example.com',
            password='SomePass123!',
            user_type='investor',
        )

        self.client.force_login(user)
        response = self.client.get(reverse('screen2'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/screen2.html')
        self.assertEqual(response.context.get('role'), 'Investor')

    def test_screen3_sets_role_from_user_type(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(
            email='university_user@example.com',
            username='university_user@example.com',
            password='SomePass123!',
            user_type='university',
        )

        self.client.force_login(user)
        response = self.client.get(reverse('screen3'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/screen3.html')
        self.assertEqual(response.context.get('role'), 'University')


class WelcomeAndPaginationEdgeTests(TestCase):
    def test_welcome_renders_template(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/welcome.html')

    def test_search_view_per_page_non_int_defaults_to_10(self):
        # Create enough opportunities to require pagination.
        Opportunity.objects.all().delete()
        for i in range(11):
            Opportunity.objects.create(name=f'Opp {i}', type='Job', category='Tech', description='x')

        response = self.client.get(reverse('opportunity_search'), {'per_page': 'abc'})
        self.assertEqual(response.status_code, 200)
        page_obj = response.context['opportunities']
        self.assertEqual(page_obj.paginator.per_page, 10)

    def test_search_view_per_page_zero_defaults_to_10(self):
        Opportunity.objects.all().delete()
        for i in range(11):
            Opportunity.objects.create(name=f'Opp {i}', type='Job', category='Tech', description='x')

        response = self.client.get(reverse('opportunity_search'), {'per_page': 0})
        self.assertEqual(response.status_code, 200)
        page_obj = response.context['opportunities']
        self.assertEqual(page_obj.paginator.per_page, 10)

    def test_search_view_per_page_negative_defaults_to_10_negative(self):
        Opportunity.objects.all().delete()
        for i in range(11):
            Opportunity.objects.create(name=f'Opp {i}', type='Job', category='Tech', description='x')

        response = self.client.get(reverse('opportunity_search'), {'per_page': -5})
        self.assertEqual(response.status_code, 200)
        page_obj = response.context['opportunities']
        self.assertEqual(page_obj.paginator.per_page, 10)

    def test_search_view_page_non_int_defaults_to_1_negative(self):
        Opportunity.objects.all().delete()
        for i in range(15):
            Opportunity.objects.create(name=f'Opp {i}', type='Job', category='Tech', description='x')

        response = self.client.get(reverse('opportunity_search'), {'per_page': 10, 'page': 'abc'})
        self.assertEqual(response.status_code, 200)
        page_obj = response.context['opportunities']
        self.assertEqual(page_obj.number, 1)

    def test_search_view_page_out_of_range_returns_last_page_negative(self):
        Opportunity.objects.all().delete()
        for i in range(25):
            Opportunity.objects.create(name=f'Opp {i}', type='Job', category='Tech', description='x')

        response = self.client.get(reverse('opportunity_search'), {'per_page': 10, 'page': 999})
        self.assertEqual(response.status_code, 200)
        page_obj = response.context['opportunities']
        self.assertEqual(page_obj.number, page_obj.paginator.num_pages)


class PerformanceQueryCountTests(TestCase):
    def test_opportunity_search_does_not_exceed_reasonable_query_count(self):
        """Performance test (stable): caps DB queries rather than timing assertions."""
        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        Opportunity.objects.all().delete()
        for i in range(50):
            Opportunity.objects.create(name=f'Python Opp {i}', type='Job', category='Tech', description='Python')

        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(reverse('opportunity_search'), {'q': 'Python', 'per_page': 10, 'page': 1})

        self.assertEqual(response.status_code, 200)
        # Typical is ~3 queries (count, paginator count, page slice). Allow a little headroom.
        self.assertLessEqual(len(ctx), 6)


class SmokeTests(TestCase):
    def test_smoke_public_pages_load(self):
        """Smoke test: critical public endpoints return 200."""
        for name in ['welcome', 'opportunity_search', 'login', 'register']:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, f'{name} should return 200')
