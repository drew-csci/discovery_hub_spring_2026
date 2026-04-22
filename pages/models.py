from django.db import models

class Opportunity(models.Model):
    STAGE_CHOICES = [
        ('early', 'Early Stage (Seed/Pre-seed)'),
        ('growth', 'Growth Stage'),
        ('mature', 'Mature'),
        ('expansion', 'Expansion'),
    ]
    
    INDUSTRY_CHOICES = [
        ('fintech', 'FinTech'),
        ('healthcare', 'Healthcare'),
        ('logistics', 'Logistics'),
        ('ai', 'AI/Machine Learning'),
        ('ecommerce', 'E-Commerce'),
        ('energy', 'Clean Energy'),
        ('biotech', 'Biotech'),
        ('software', 'Software'),
        ('other', 'Other'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True, default='')
    category = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    
    # Company Details
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='other')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='early')
    founded_year = models.IntegerField(default=2024)
    
    # Metrics
    patent_count = models.IntegerField(default=0)
    revenue_annual = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    employee_count = models.IntegerField(default=0)
    
    # Funding
    funding_needed = models.DecimalField(max_digits=15, decimal_places=2, default=100000)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

