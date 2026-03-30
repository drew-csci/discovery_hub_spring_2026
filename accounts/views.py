from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User
from .forms import (
    UserRegistrationForm,
    EmailLoginForm,
    PasswordResetRequestForm,
    ResetPasswordForm
)


@require_http_methods(["GET", "POST"])
def register(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    
    # Get user type from query parameter
    user_type = request.GET.get('type', '')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Discovery Hub.')
            
            # Redirect based on user type
            if user.user_type == 'company':
                return redirect('pages:company_dashboard')
            return redirect('pages:screen1')
    else:
        form = UserRegistrationForm()
        # Pre-select user type if provided
        if user_type in dict(form.fields['user_type'].choices):
            form.fields['user_type'].initial = user_type
    
    context = {
        'form': form,
        'user_type': user_type
    }
    return render(request, 'accounts/register.html', context)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.display_name}!')
                    
                    # Redirect based on user type
                    if user.user_type == 'company':
                        return redirect('pages:company_dashboard')
                    return redirect('pages:screen1')
                else:
                    messages.error(request, 'Invalid email or password')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password')
    else:
        form = EmailLoginForm()
    
    user_type = request.GET.get('type')
    context = {'form': form, 'selected_user_type': user_type}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["POST"])
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('pages:index')


@require_http_methods(["GET", "POST"])
def password_reset_request(request):
    """Request password reset"""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # TODO: Implement email sending with token
                messages.info(request, 'Check your email for password reset instructions.')
            except User.DoesNotExist:
                # Don't reveal if email exists
                messages.info(request, 'Check your email for password reset instructions.')
            return redirect('accounts:login')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset_form.html', {'form': form})


@require_http_methods(["GET", "POST"])
def password_reset(request, token=None):
    """Reset password with token"""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    
    # TODO: Implement token verification
    user = None
    
    if not user:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('accounts:login')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your password has been reset. You can now log in.')
            return redirect('accounts:login')
    else:
        form = ResetPasswordForm()
    
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})
