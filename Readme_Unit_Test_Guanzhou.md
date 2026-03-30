# Unit Tests Documentation - Innovation Feed Feature

## Overview
This document explains the comprehensive unit test suite for the Innovation Feed feature, covering view testing, form validation, authentication, authorization, and media handling.

## Test Structure

### Test Class: `InnovationFeedViewTests`
Located in `pages/tests.py`, this test class contains 15 unit tests organized into two main categories:

## 1. Feed View Tests (`feed()` function)

### `test_feed_view_requires_login`
**Purpose**: Ensures the feed view requires user authentication
```python
def test_feed_view_requires_login(self):
    response = self.client.get(reverse('feed'))
    self.assertRedirects(response, f"{reverse('login')}?next={reverse('feed')}")
```
**What it tests**:
- Unauthenticated users cannot access `/feed/`
- Redirects to login page with `next` parameter
- Uses Django's `@login_required` decorator

### `test_feed_view_authenticated_user_can_access`
**Purpose**: Verifies authenticated users can view the feed
```python
def test_feed_view_authenticated_user_can_access(self):
    self.client.login(email='company@example.com', password='pass12345')
    response = self.client.get(reverse('feed'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'pages/feed.html')
```
**What it tests**:
- Authenticated users get HTTP 200 response
- Correct template (`pages/feed.html`) is rendered
- View is accessible to logged-in users

### `test_feed_view_shows_all_posts`
**Purpose**: Confirms feed displays all posts in the database
```python
def test_feed_view_shows_all_posts(self):
    # Create additional post
    Post.objects.create(...)
    self.client.login(email='company@example.com', password='pass12345')
    response = self.client.get(reverse('feed'))
    self.assertEqual(len(response.context['posts']), 2)
```
**What it tests**:
- All posts are retrieved (`Post.objects.all()`)
- Posts are passed to template context
- Multiple posts are displayed correctly

### `test_feed_view_empty_when_no_posts`
**Purpose**: Tests empty state when no posts exist
```python
def test_feed_view_empty_when_no_posts(self):
    self.test_post.delete()  # Remove existing post
    response = self.client.get(reverse('feed'))
    self.assertEqual(len(response.context['posts']), 0)
    self.assertContains(response, 'No posts yet')
```
**What it tests**:
- Empty queryset handling
- Template displays appropriate empty state message
- Context contains empty posts list

### `test_feed_view_posts_ordered_by_newest_first`
**Purpose**: Validates chronological ordering of posts
```python
def test_feed_view_posts_ordered_by_newest_first(self):
    time.sleep(0.1)  # Ensure timestamp difference
    newer_post = Post.objects.create(...)
    response = self.client.get(reverse('feed'))
    posts = list(response.context['posts'])
    self.assertEqual(posts[0].title, 'Newer Post')
```
**What it tests**:
- Posts ordered by `created_at` descending (model's `Meta.ordering`)
- Newest posts appear first in feed
- Template receives correctly ordered queryset

## 2. Create Post View Tests (`create_post()` function)

### Authentication & Authorization Tests

#### `test_create_post_view_requires_login`
**Purpose**: Ensures create post view requires authentication
```python
def test_create_post_view_requires_login(self):
    response = self.client.get(reverse('create_post'))
    self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_post')}")
```
**What it tests**:
- Unauthenticated GET requests redirect to login
- `@login_required` decorator functions correctly

#### `test_create_post_get_request_company_user`
**Purpose**: Verifies company users can access create post form
```python
def test_create_post_get_request_company_user(self):
    self.client.login(email='company@example.com', password='pass12345')
    response = self.client.get(reverse('create_post'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'pages/create_post.html')
    self.assertIsInstance(response.context['form'], PostForm)
```
**What it tests**:
- Company users get HTTP 200 for GET requests
- Correct template rendered
- Form instance provided in context

#### `test_create_post_get_request_university_user`
**Purpose**: Confirms university users can access create post form
```python
def test_create_post_get_request_university_user(self):
    self.client.login(email='university@example.com', password='pass12345')
    response = self.client.get(reverse('create_post'))
    self.assertEqual(response.status_code, 200)
```
**What it tests**:
- University users have same access as company users
- Role-based permissions work for authorized roles

#### `test_create_post_get_request_investor_user_blocked`
**Purpose**: Ensures investor users are blocked from creating posts
```python
def test_create_post_get_request_investor_user_blocked(self):
    self.client.login(email='investor@example.com', password='pass12345')
    response = self.client.get(reverse('create_post'), follow=True)
    self.assertRedirects(response, reverse('feed'))
    self.assertContains(response, 'Only Company and University users can create posts')
```
**What it tests**:
- Investor role authorization check
- Redirect to feed with error message
- Message persistence across redirects

### Form Submission Tests

#### `test_create_post_successful_submission`
**Purpose**: Tests successful post creation with valid data
```python
def test_create_post_successful_submission(self):
    self.client.login(email='company@example.com', password='pass12345')
    post_data = {'title': 'New Innovation Post', 'description': '...'}
    response = self.client.post(reverse('create_post'), post_data, follow=True)
    self.assertRedirects(response, reverse('feed'))
    self.assertContains(response, 'Post created successfully')
    # Database verification
    post = Post.objects.get(title='New Innovation Post')
    self.assertEqual(post.author, self.company_user)
```
**What it tests**:
- Valid POST data creates post successfully
- Redirect to feed after creation
- Success message displayed
- Post saved to database with correct author
- Organization fields auto-populated

#### `test_create_post_with_media_file`
**Purpose**: Tests post creation with image upload
```python
def test_create_post_with_media_file(self):
    img = SimpleUploadedFile('test.png', b'\x89PNG\r\n\x1a\n', content_type='image/png')
    post_data = {'title': 'Post with Image', 'media': img}
    response = self.client.post(reverse('create_post'), post_data, follow=True)
    post = Post.objects.get(title='Post with Image')
    self.assertEqual(post.media_type, 'image')
```
**What it tests**:
- File upload handling
- Media type auto-detection (image)
- File storage in `post_media/` directory
- Media field population

#### `test_create_post_with_video_file`
**Purpose**: Tests post creation with video upload
```python
def test_create_post_with_video_file(self):
    video = SimpleUploadedFile('test.mp4', b'fake video content', content_type='video/mp4')
    post_data = {'title': 'Post with Video', 'media': video}
    response = self.client.post(reverse('create_post'), post_data, follow=True)
    post = Post.objects.get(title='Post with Video')
    self.assertEqual(post.media_type, 'video')
```
**What it tests**:
- Video file upload processing
- Media type detection by file extension
- Organization type preservation

### Form Validation Tests

#### `test_create_post_missing_required_title`
**Purpose**: Tests validation when required title is missing
```python
def test_create_post_missing_required_title(self):
    post_data = {'description': 'Missing title should fail'}
    response = self.client.post(reverse('create_post'), post_data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'pages/create_post.html')
    self.assertContains(response, 'This field is required')
```
**What it tests**:
- Django ModelForm validation for required fields
- Form errors displayed in template
- No redirect on validation failure

#### `test_create_post_oversized_file`
**Purpose**: Tests file size validation (>20MB)
```python
def test_create_post_oversized_file(self):
    large_file = SimpleUploadedFile('large.png', b'x' * (21 * 1024 * 1024), content_type='image/png')
    post_data = {'title': 'Large File Test', 'media': large_file}
    response = self.client.post(reverse('create_post'), post_data)
    self.assertContains(response, 'Media file must be below 20MB')
```
**What it tests**:
- Custom form validation in `PostForm.clean_media()`
- File size limit enforcement (20MB)
- Error message display

#### `test_create_post_invalid_file_type`
**Purpose**: Tests file type validation (only images/videos allowed)
```python
def test_create_post_invalid_file_type(self):
    text_file = SimpleUploadedFile('test.txt', b'text content', content_type='text/plain')
    post_data = {'title': 'Invalid File Type', 'media': text_file}
    response = self.client.post(reverse('create_post'), post_data)
    self.assertContains(response, 'Only image or video files are allowed')
```
**What it tests**:
- MIME type validation in form
- Content type checking (`image/*`, `video/*`)
- Rejection of invalid file types

#### `test_create_post_investor_blocked_on_post`
**Purpose**: Tests POST authorization for investor users
```python
def test_create_post_investor_blocked_on_post(self):
    self.client.login(email='investor@example.com', password='pass12345')
    post_data = {'title': 'Investor Post Attempt'}
    response = self.client.post(reverse('create_post'), post_data, follow=True)
    self.assertRedirects(response, reverse('feed'))
    self.assertFalse(Post.objects.filter(title='Investor Post Attempt').exists())
```
**What it tests**:
- POST request authorization check
- Investor role blocked from creating posts
- No post created in database
- Proper redirect and error message

## Test Setup & Fixtures

### `setUp()` Method
```python
def setUp(self):
    # Create test users with different roles
    self.company_user = User.objects.create_user(...)
    self.university_user = User.objects.create_user(...)
    self.investor_user = User.objects.create_user(...)

    # Create initial test post
    self.test_post = Post.objects.create(...)
```
**Purpose**:
- Creates consistent test data for each test
- Provides users with different roles for authorization testing
- Ensures clean database state per test

## Testing Methodology

### Django Test Client
- Uses `self.client` for HTTP request simulation
- Tests complete request-response cycle
- Validates templates, context, and redirects

### Authentication Testing
- `self.client.login()` for user authentication
- Tests `@login_required` decorator behavior
- Validates role-based access control

### Database Testing
- Creates test data in `setUp()`
- Verifies database state after operations
- Tests model relationships and field population

### Form Testing
- Tests both GET (form display) and POST (form submission)
- Validates form validation and error handling
- Tests file upload processing

### Template Testing
- Verifies correct template rendering
- Checks context data availability
- Validates conditional template logic

## Running the Tests

### Run All View Tests
```bash
python manage.py test pages.tests.InnovationFeedViewTests
```

### Run Specific Test
```bash
python manage.py test pages.tests.InnovationFeedViewTests.test_feed_view_requires_login
```

### Run with Verbose Output
```bash
python manage.py test pages.tests.InnovationFeedViewTests --verbosity=2
```

## Test Coverage Summary

| Category | Tests | Coverage |
|----------|-------|----------|
| Authentication | 2 | Login requirements for both views |
| Authorization | 4 | Role-based access (Company/University vs Investor) |
| Feed Display | 5 | Post listing, ordering, empty states |
| Form Validation | 3 | Required fields, file size, file type |
| Media Handling | 2 | Image/video upload and type detection |
| Database Operations | 5 | Post creation, field population, relationships |
| **Total** | **15** | **Complete view layer coverage** |

## Key Testing Principles Applied

1. **Isolation**: Each test is independent with clean database state
2. **Realism**: Tests simulate actual user interactions via test client
3. **Completeness**: Covers happy path, error cases, and edge conditions
4. **Readability**: Clear test names and docstrings explain purpose
5. **Maintainability**: Uses fixtures and helper methods for consistency

## Test Dependencies

- Django's `TestCase` and test client
- `django.urls.reverse()` for URL resolution
- `django.core.files.uploadedfile.SimpleUploadedFile` for file uploads
- Custom `User` and `Post` models
- `PostForm` for form validation

---
**Author**: Guanzhou Shen (Unit Test Documentation)
**Date**: March 30, 2026
**Test Class**: `InnovationFeedViewTests`
**Total Tests**: 15 unit tests</content>
<parameter name="filePath">C:\Users\56399\OneDrive\桌面\Drew\discovery_hub_2026\discovery_hub_spring_2026\Readme_Unit_Test_Guanzhou.md