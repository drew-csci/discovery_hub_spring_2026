"""Django forms for accounts app"""

from django import forms
from django.core.exceptions import ValidationError
from .models import User


class UserRegistrationForm(forms.ModelForm):
    """User registration form"""
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        min_length=8
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput()
    )
    
    class Meta:
        model = User
        fields = ('email', 'user_type', 'first_name', 'last_name')
        widgets = {
            'user_type': forms.Select(choices=[
                ('university', 'University / TTO'),
                ('company', 'Company'),
                ('investor', 'Investor')
            ])
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered. Please log in or use a different email.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords must match.")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class EmailLoginForm(forms.Form):
    """Email login form"""
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    remember_me = forms.BooleanField(required=False, label='Remember Me')


class PasswordResetRequestForm(forms.Form):
    """Password reset request form"""
    email = forms.EmailField(label='Email')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise ValidationError('No account found with that email address.')
        except User.DoesNotExist:
            raise ValidationError('No account found with that email address.')
        return email


class ResetPasswordForm(forms.Form):
    """Reset password form"""
    password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(),
        min_length=8
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput()
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords must match.")
        return cleaned_data
