from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    industry = models.CharField(max_length=128, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=128, blank=True)
    domain = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Patent(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField(blank=True)
    owner_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='patents')
    owner_university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True, related_name='patents')
    filed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=64, choices=[
        ('filed', 'Filed'),
        ('pending', 'Pending'),
        ('granted', 'Granted'),
        ('expired', 'Expired'),
    ], default='filed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-filed_date', 'title']

    def __str__(self):
        return self.title


class SystemSetting(models.Model):
    key = models.CharField(max_length=128, unique=True)
    value = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return f"{self.key}={self.value}"

    @classmethod
    def get_value(cls, key, default=None):
        try:
            item = cls.objects.get(key=key, is_active=True)
            return item.value
        except cls.DoesNotExist:
            return default

