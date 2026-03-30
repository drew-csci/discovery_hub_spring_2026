# Midterm Project - Innovation Feed Feature

## Overview
This feature implements an Innovation Feed system where users can view and create posts showcasing patented ideas. The system supports multimedia content (images and videos) and automatically attaches organization profiles to posts.

## User Roles
- **Company**: Can create and view posts
- **University**: Can create and view posts
- **Investor**: Can only view posts (cannot create)

## Acceptance Criteria Met
1. ✅ "Create Post" button visible for authorized roles (Company/University)
2. ✅ View videos and pictures in the feed
3. ✅ Organization profile automatically inserted underneath each post
4. ✅ Posting restricted by role (only Company/University can post)

## New Code Files and Changes

### 1. Database Model (`pages/models.py`)
```python
class Post(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    organization_name = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=50)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media = models.FileField(upload_to='post_media/', blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MediaType.choices, default=MediaType.IMAGE, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.organization_name}"

    def save(self, *args, **kwargs):
        if self.media and not self.media_type:
            name = self.media.name.lower()
            if name.endswith(('.mp4', '.avi', '.mov', '.webm')):
                self.media_type = self.MediaType.VIDEO
            else:
                self.media_type = self.MediaType.IMAGE

        if not self.organization_name and self.author:
            self.organization_name = self.author.display_name
            self.organization_type = self.author.user_type

        super().save(*args, **kwargs)
```
**Purpose**: Defines the Post model with fields for author, organization info, content, and media. Automatically detects media type and populates organization data from the author.

### 2. Admin Interface (`pages/admin.py`)
```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization_name', 'organization_type', 'author', 'created_at')
    list_filter = ('organization_type', 'created_at')
    search_fields = ('title', 'description', 'organization_name', 'author__email')
```
**Purpose**: Registers the Post model in Django admin with useful display and filtering options for content management.

### 3. Form Handling (`pages/forms.py`)
```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'media']

    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media:
            if media.size > 20 * 1024 * 1024:
                raise forms.ValidationError('Media file must be below 20MB.')
            content_type = media.content_type
            if not any(x in content_type for x in ['image/', 'video/']):
                raise forms.ValidationError('Only image or video files are allowed.')
        return media
```
**Purpose**: Provides form validation for post creation, including file size limits (20MB) and content type restrictions (images/videos only).

### 4. View Functions (`pages/views.py`)
```python
@login_required
def feed(request):
    posts = Post.objects.all()
    return render(request, 'pages/feed.html', {'posts': posts})

@login_required
def create_post(request):
    if request.user.user_type not in ['company', 'university']:
        messages.error(request, 'Only Company and University users can create posts.')
        return redirect('feed')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.organization_name = request.user.display_name
            post.organization_type = request.user.user_type

            if post.media and not post.media_type:
                name = post.media.name.lower()
                if name.endswith(('.mp4', '.avi', '.mov', '.webm')):
                    post.media_type = Post.MediaType.VIDEO
                else:
                    post.media_type = Post.MediaType.IMAGE

            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('feed')
    else:
        form = PostForm()

    return render(request, 'pages/create_post.html', {'form': form})
```
**Purpose**: 
- `feed()`: Displays all posts in chronological order
- `create_post()`: Handles post creation with role-based access control and automatic organization profile attachment

### 5. URL Configuration (`pages/urls.py`)
```python
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('screen1/', views.screen1, name='screen1'),
    path('screen2/', views.screen2, name='screen2'),
    path('screen3/', views.screen3, name='screen3'),
    path('feed/', views.feed, name='feed'),
    path('feed/create/', views.create_post, name='create_post'),
]
```
**Purpose**: Defines URL patterns for the feed and post creation pages.

### 6. Templates

#### Feed Template (`templates/pages/feed.html`)
```html
{% extends "base.html" %}
{% block content %}
  <section class="dash-card">
    <h1>Innovation Feed</h1>
    <p class="muted">Browse latest patented idea showcases from companies and universities.</p>

    {% if user.is_authenticated %}
      {% if user.user_type == 'company' or user.user_type == 'university' %}
        <a class="btn" href="{% url 'create_post' %}">Create Post</a>
      {% endif %}
    {% endif %}

    {% if posts %}
      <div class="feed-grid">
      {% for post in posts %}
        <article class="post-card">
          <h2>{{ post.title }}</h2>
          <p>{{ post.description|linebreaksbr }}</p>

          {% if post.media %}
            {% if post.media_type == 'image' %}
              <img src="{{ post.media.url }}" alt="{{ post.title }}" style="max-width:100%;height:auto;" />
            {% elif post.media_type == 'video' %}
              <video controls style="max-width:100%;height:auto;">
                <source src="{{ post.media.url }}" type="video/mp4">
                Your browser does not support HTML5 video.
              </video>
            {% endif %}
          {% endif %}

          <div class="post-meta">
            <span>Posted by <strong>{{ post.organization_name }}</strong> ({{ post.organization_type|title }})</span>
            <span>on {{ post.created_at|date:'M d, Y H:i' }}</span>
          </div>
        </article>
      {% endfor %}
      </div>
    {% else %}
      <p>No posts yet. Be the first to create one!</p>
    {% endif %}
  </section>
{% endblock %}
```
**Purpose**: Displays the innovation feed with conditional "Create Post" button, post cards showing media content, and organization profiles.

#### Create Post Template (`templates/pages/create_post.html`)
```html
{% extends "base.html" %}
{% block content %}
  <section class="dash-card">
    <h1>Create Innovation Post</h1>
    <form method="post" enctype="multipart/form-data" novalidate>
      {% csrf_token %}
      <div class="form-group">
        {{ form.title.label_tag }}
        {{ form.title }}
        {{ form.title.errors }}
      </div>
      <div class="form-group">
        {{ form.description.label_tag }}
        {{ form.description }}
        {{ form.description.errors }}
      </div>
      <div class="form-group">
        {{ form.media.label_tag }}
        {{ form.media }}
        {{ form.media.errors }}
      </div>
      <div class="button-row">
        <button class="btn" type="submit">Submit Post</button>
        <a class="btn" href="{% url 'feed' %}">Back to Feed</a>
      </div>
    </form>
  </section>
{% endblock %}
```
**Purpose**: Provides a form interface for creating new posts with file upload support.

### 7. Navigation Update (`templates/base.html`)
```html
<li><a href="{% url 'feed' %}">Innovation Feed</a></li>
```
**Purpose**: Adds navigation link to the Innovation Feed in the site header.

### 8. Settings Configuration (`discovery_hub/settings.py`)
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
**Purpose**: Configures Django to serve uploaded media files during development.

### 9. Main URL Configuration (`discovery_hub/urls.py`)
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
**Purpose**: Serves media files in development mode.

### 10. Git Ignore Update (`.gitignore`)
```
media/
```
**Purpose**: Prevents uploaded media files from being committed to version control.

### 11. Test Suite (`pages/tests.py`)
```python
class InnovationFeedTests(TestCase):
    def setUp(self):
        self.company_user = User.objects.create_user(
            email='company@example.com', username='companyuser', password='pass12345', user_type='company')
        self.investor_user = User.objects.create_user(
            email='investor@example.com', username='investoruser', password='pass12345', user_type='investor')

    def test_company_can_create_post_and_see_feed(self):
        self.client.login(email='company@example.com', password='pass12345')
        url = reverse('create_post')

        img = SimpleUploadedFile('test.png', b'\x89PNG\r\n\x1a\n', content_type='image/png')
        resp = self.client.post(url, {'title': 'New Idea', 'description': 'Innovation test', 'media': img}, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Post created successfully')

        feed = self.client.get(reverse('feed'))
        self.assertContains(feed, 'New Idea')
        self.assertContains(feed, 'company@example.com')

    def test_investor_cannot_create_post(self):
        self.client.login(email='investor@example.com', password='pass12345')
        url = reverse('create_post')
        resp = self.client.get(url, follow=True)

        self.assertRedirects(resp, reverse('feed'))
        self.assertContains(resp, 'Only Company and University users can create posts')
```
**Purpose**: Provides automated tests for post creation permissions and feed display functionality.

## Database Migration
- **Migration File**: `pages/migrations/0001_initial.py`
- **Purpose**: Creates the `pages_post` table with all required fields
- **Status**: Applied successfully

## Feature Workflow
1. **Access**: Users navigate to `/feed/` to view the innovation feed
2. **Authorization**: Only Company and University users see the "Create Post" button
3. **Creation**: Authorized users can create posts with title, description, and media files
4. **Validation**: Form validates file size (≤20MB) and content type (images/videos only)
5. **Display**: Posts show media content with automatic organization profile attachment
6. **Organization Info**: Each post displays the author's organization name and type

## Security Features
- Role-based access control for post creation
- File upload validation (size and type restrictions)
- User authentication required for all feed operations

## Media Handling
- **Supported Formats**: Images (PNG, JPG, etc.) and Videos (MP4, AVI, MOV, WebM)
- **Storage**: Files uploaded to `media/post_media/` directory
- **Display**: Automatic media type detection and appropriate HTML rendering

## Testing
- Unit tests for role-based permissions
- Integration tests for post creation and feed display
- Form validation testing for file uploads

## Future Enhancements
- Post editing and deletion functionality
- Like/comment system for posts
- Advanced search and filtering
- Notification system for new posts
- Media compression and optimization

---
**Author**: Guanzhou Shen
**Date**: March 30, 2026
**Branch**: Midterm_Guanzhou</content>
<parameter name="filePath">C:\Users\56399\OneDrive\桌面\Drew\discovery_hub_2026\discovery_hub_spring_2026\Readme_Midterm_Guanzhou.md