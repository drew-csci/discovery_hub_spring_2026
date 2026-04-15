from django.contrib import admin
from .models import Company, University, Patent, SystemSetting


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'website', 'created_at', 'updated_at')
    search_fields = ('name', 'industry')
    list_filter = ('industry',)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'domain', 'created_at', 'updated_at')
    search_fields = ('name', 'country', 'domain')
    list_filter = ('country',)


@admin.register(Patent)
class PatentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner_company', 'owner_university', 'filed_date', 'status')
    search_fields = ('title', 'abstract')
    list_filter = ('status',)


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'is_active', 'updated_at')
    search_fields = ('key', 'value')
    list_filter = ('is_active',)

