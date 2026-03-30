from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(AbstractUser):
    """Custom user model for authentication"""
    
    USER_TYPES = ['university', 'company', 'investor']
    USER_TYPE_CHOICES = [
        ('university', 'University'),
        ('company', 'Company'),
        ('investor', 'Investor'),
    ]
    
    email = models.EmailField(unique=True, max_length=255, db_index=True)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='university'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'accounts_user'
    
    def __str__(self):
        return self.email
    
    @property
    def display_name(self):
        """Return full name or email"""
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.email
    
    @property
    def is_university(self):
        return self.user_type == 'university'
    
    @property
    def is_company(self):
        return self.user_type == 'company'
    
    @property
    def is_investor(self):
        return self.user_type == 'investor'


class TTOProfile(models.Model):
    """Technology Transfer Office profile for university users"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ttoprofile')
    institution_name = models.CharField(max_length=255, blank=True, default='')
    office_name = models.CharField(max_length=255, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    therapeutic_focus_tags = models.JSONField(default=list, blank=True)
    trl_range_interest_min = models.IntegerField(null=True, blank=True)
    trl_range_interest_max = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tto_profiles'
    
    def __str__(self):
        return f"TTO Profile for {self.user.display_name}"


class CompanyProfile(models.Model):
    """Company profile for companies seeking funding"""
    
    STAGE_CHOICES = [
        ('new', 'New'),
        ('experienced', 'Experienced'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True, default='')
    patent_count = models.IntegerField(default=0)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='new')
    seeking_funding = models.BooleanField(default=True)
    description = models.TextField(blank=True, default='')
    funding_details = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'company_profiles'
    
    def __str__(self):
        return self.company_name
