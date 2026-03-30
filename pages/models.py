from django.db import models


class Page(models.Model):
    """Page model for managing page content"""
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(blank=True, default='')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pages'
    
    def __str__(self):
        return self.title
