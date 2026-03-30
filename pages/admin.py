from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization_name', 'organization_type', 'author', 'created_at')
    list_filter = ('organization_type', 'created_at')
    search_fields = ('title', 'description', 'organization_name', 'author__email')
