from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post
from .forms import PostForm


def welcome(request):
    return render(request, 'pages/welcome.html')

@login_required
def screen1(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen1.html', {'role': role})

@login_required
def screen2(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen2.html', {'role': role})

@login_required
def screen3(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen3.html', {'role': role})

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

            # Set organization info - use display_name if user has set proper name, otherwise leave empty
            display_name = request.user.display_name
            if display_name and display_name != request.user.email:
                post.organization_name = display_name
            # organization_type is always set to user's type
            post.organization_type = request.user.user_type

            if post.media and (not post.media_type or post.media_type == Post.MediaType.IMAGE):
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

