from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import User
from .models import Post
from .forms import PostForm


class InnovationFeedViewTests(TestCase):
    def setUp(self):
        # Create test users
        self.company_user = User.objects.create_user(
            email='company@example.com', username='companyuser', password='pass12345', user_type='company')
        self.university_user = User.objects.create_user(
            email='university@example.com', username='universityuser', password='pass12345', user_type='university')
        self.investor_user = User.objects.create_user(
            email='investor@example.com', username='investoruser', password='pass12345', user_type='investor')

        # Create test post
        self.test_post = Post.objects.create(
            author=self.company_user,
            organization_name='Test Company',
            organization_type='company',
            title='Test Innovation',
            description='A test post description'
        )

    # ===== FEED VIEW TESTS =====

    def test_feed_view_requires_login(self):
        """Test that feed view redirects unauthenticated users to login."""
        response = self.client.get(reverse('feed'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('feed')}")

    def test_feed_view_authenticated_user_can_access(self):
        """Test that authenticated users can access the feed."""
        self.client.login(email='company@example.com', password='pass12345')
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/feed.html')

    def test_feed_view_shows_all_posts(self):
        """Test that feed displays all posts in context."""
        # Create another post
        Post.objects.create(
            author=self.university_user,
            organization_name='Test University',
            organization_type='university',
            title='University Innovation',
            description='Another test post'
        )

        self.client.login(email='company@example.com', password='pass12345')
        response = self.client.get(reverse('feed'))

        # Check that both posts are in context
        self.assertEqual(len(response.context['posts']), 2)
        post_titles = [post.title for post in response.context['posts']]
        self.assertIn('Test Innovation', post_titles)
        self.assertIn('University Innovation', post_titles)

    def test_feed_view_empty_when_no_posts(self):
        """Test that feed shows empty state when no posts exist."""
        # Delete the test post
        self.test_post.delete()

        self.client.login(email='company@example.com', password='pass12345')
        response = self.client.get(reverse('feed'))

        self.assertEqual(len(response.context['posts']), 0)
        self.assertContains(response, 'No posts yet')

    def test_feed_view_posts_ordered_by_newest_first(self):
        """Test that posts are ordered by creation date (newest first)."""
        # Create a newer post
        import time
        time.sleep(0.1)  # Ensure different timestamp
        newer_post = Post.objects.create(
            author=self.university_user,
            organization_name='Test University',
            organization_type='university',
            title='Newer Post',
            description='This should appear first'
        )

        self.client.login(email='company@example.com', password='pass12345')
        response = self.client.get(reverse('feed'))

        posts = list(response.context['posts'])
        self.assertEqual(posts[0].title, 'Newer Post')  # Newest first
        self.assertEqual(posts[1].title, 'Test Innovation')  # Older second

    # ===== CREATE_POST VIEW TESTS =====

    def test_create_post_view_requires_login(self):
        """Test that create_post view redirects unauthenticated users."""
        response = self.client.get(reverse('create_post'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_post')}")

    def test_create_post_get_request_company_user(self):
        """Test GET request to create_post for company user."""
        self.client.login(email='company@example.com', password='pass12345')
        response = self.client.get(reverse('create_post'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_post.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_create_post_get_request_university_user(self):
        """Test GET request to create_post for university user."""
        self.client.login(email='university@example.com', password='pass12345')
        response = self.client.get(reverse('create_post'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_post.html')

    def test_create_post_get_request_investor_user_blocked(self):
        """Test that investor users are blocked from create_post GET."""
        self.client.login(email='investor@example.com', password='pass12345')
        response = self.client.get(reverse('create_post'), follow=True)

        self.assertRedirects(response, reverse('feed'))
        self.assertContains(response, 'Only Company and University users can create posts')

    def test_create_post_successful_submission(self):
        """Test successful post creation with valid data."""
        self.client.login(email='company@example.com', password='pass12345')

        post_data = {
            'title': 'New Innovation Post',
            'description': 'This is a great innovation!'
        }

        response = self.client.post(reverse('create_post'), post_data, follow=True)

        self.assertRedirects(response, reverse('feed'))
        self.assertContains(response, 'Post created successfully')

        # Verify post was created in database
        post = Post.objects.get(title='New Innovation Post')
        self.assertEqual(post.author, self.company_user)
        # For users without proper names, organization_name should be empty
        self.assertEqual(post.organization_name, '')
        self.assertEqual(post.organization_type, 'company')

    def test_create_post_with_media_file(self):
        """Test post creation with media file upload."""
        self.client.login(email='company@example.com', password='pass12345')

        # Create a test image file
        img = SimpleUploadedFile('test.png', b'\x89PNG\r\n\x1a\n', content_type='image/png')

        post_data = {
            'title': 'Post with Image',
            'description': 'Testing media upload',
            'media': img
        }

        response = self.client.post(reverse('create_post'), post_data, follow=True)

        self.assertRedirects(response, reverse('feed'))
        self.assertContains(response, 'Post created successfully')

        # Verify post and media type
        post = Post.objects.get(title='Post with Image')
        self.assertEqual(post.media_type, 'image')
        self.assertTrue(post.media.name.endswith('.png'))

    def test_create_post_with_video_file(self):
        """Test post creation with video file upload."""
        self.client.login(email='university@example.com', password='pass12345')

        # Create a test video file
        video = SimpleUploadedFile('test.mp4', b'fake video content', content_type='video/mp4')

        post_data = {
            'title': 'Post with Video',
            'description': 'Testing video upload',
            'media': video
        }

        response = self.client.post(reverse('create_post'), post_data, follow=True)

        self.assertRedirects(response, reverse('feed'))

        # Verify post and media type detection
        post = Post.objects.get(title='Post with Video')
        self.assertEqual(post.media_type, 'video')
        self.assertEqual(post.organization_type, 'university')

    def test_create_post_missing_required_title(self):
        """Test post creation fails with missing title."""
        self.client.login(email='company@example.com', password='pass12345')

        post_data = {
            'description': 'Missing title should fail'
        }

        response = self.client.post(reverse('create_post'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_post.html')
        self.assertContains(response, 'This field is required')

    def test_create_post_oversized_file(self):
        """Test post creation fails with file over 20MB."""
        self.client.login(email='company@example.com', password='pass12345')

        # Create a file larger than 20MB (simulate)
        large_file = SimpleUploadedFile('large.png', b'x' * (21 * 1024 * 1024), content_type='image/png')

        post_data = {
            'title': 'Large File Test',
            'media': large_file
        }

        response = self.client.post(reverse('create_post'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_post.html')
        self.assertContains(response, 'Media file must be below 20MB')

    def test_create_post_invalid_file_type(self):
        """Test post creation fails with invalid file type."""
        self.client.login(email='company@example.com', password='pass12345')

        # Create a text file (invalid type)
        text_file = SimpleUploadedFile('test.txt', b'text content', content_type='text/plain')

        post_data = {
            'title': 'Invalid File Type',
            'media': text_file
        }

        response = self.client.post(reverse('create_post'), post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_post.html')
        self.assertContains(response, 'Only image or video files are allowed')

    def test_create_post_investor_blocked_on_post(self):
        """Test that investor users are blocked from POST submissions."""
        self.client.login(email='investor@example.com', password='pass12345')

        post_data = {
            'title': 'Investor Post Attempt',
            'description': 'This should be blocked'
        }

        response = self.client.post(reverse('create_post'), post_data, follow=True)

        self.assertRedirects(response, reverse('feed'))
        self.assertContains(response, 'Only Company and University users can create posts')

        # Verify no post was created
        self.assertFalse(Post.objects.filter(title='Investor Post Attempt').exists())


class InnovationFeedIntegrationTests(TestCase):
    """Integration tests for complete user workflows."""

    def test_user_registration_to_post_creation_flow(self):
        """
        Integration test: Complete user journey from registration to post creation and feed viewing.
        Tests the end-to-end flow: register → login (automatic) → create post → view in feed.
        """
        # Step 1: User Registration
        registration_data = {
            'email': 'newcompany@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'user_type': 'company'
        }

        # Submit registration form
        response = self.client.post(reverse('register'), registration_data, follow=True)

        # Verify registration success - should redirect to screen1 and user should be logged in
        self.assertRedirects(response, reverse('screen1'))

        # Verify user was created and is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        user = response.wsgi_request.user
        self.assertEqual(user.email, 'newcompany@example.com')
        self.assertEqual(user.user_type, 'company')

        # Step 2: Create a Post (user should still be logged in from registration)
        post_data = {
            'title': 'My First Innovation Post',
            'description': 'This is my innovative idea that I want to share with the world!'
        }

        # Submit post creation form
        response = self.client.post(reverse('create_post'), post_data, follow=True)

        # Verify post creation success - should redirect to feed with success message
        self.assertRedirects(response, reverse('feed'))
        self.assertContains(response, 'Post created successfully')

        # Step 3: Verify Post in Feed
        # Access the feed (should still be logged in)
        response = self.client.get(reverse('feed'))

        # Verify feed loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/feed.html')

        # Verify post appears in feed context
        posts = response.context['posts']
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, 'My First Innovation Post')
        self.assertEqual(post.description, 'This is my innovative idea that I want to share with the world!')
        self.assertEqual(post.author, user)
        self.assertEqual(post.organization_type, 'company')
        # Organization name should be empty for new users (not set in profile yet)
        self.assertEqual(post.organization_name, '')

        # Verify post appears in template
        self.assertContains(response, 'My First Innovation Post')
        self.assertContains(response, 'This is my innovative idea that I want to share with the world!')

        # Step 4: Verify Database State
        # Check that post was actually saved to database
        db_post = Post.objects.get(title='My First Innovation Post')
        self.assertEqual(db_post.author, user)
        self.assertEqual(db_post.organization_type, 'company')
        self.assertIsNotNone(db_post.created_at)

        # Step 5: Test Post Creation Button Visibility
        # Company users should see the "Create Post" button
        response = self.client.get(reverse('feed'))
        self.assertContains(response, 'Create Post')  # Button should be visible

        # Step 6: Test Logout and Re-login Flow
        # Logout
        self.client.logout()

        # Try to access feed without login - should redirect to login
        response = self.client.get(reverse('feed'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('feed')}")

        # Login again
        login_success = self.client.login(email='newcompany@example.com', password='testpass123')
        self.assertTrue(login_success)

        # Should be able to access feed again
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)  # Post should still be there
