from django.db import models


class Opportunity(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True, default='')
    category = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class InventionDisclosure(models.Model):
    PATENT_STATUS_CHOICES = [
        ('none', 'No patent filed'),
        ('pending', 'Patent pending'),
        ('granted', 'Patent granted'),
    ]

    inventor_name = models.CharField(max_length=255)
    inventor_email = models.EmailField()
    invention_title = models.CharField(max_length=255)
    invention_description = models.TextField()
    technology_field = models.CharField(max_length=255, blank=True, default='')
    date_of_invention = models.DateField()
    inventors = models.TextField(blank=True, default='')
    patent_status = models.CharField(
        max_length=20,
        choices=PATENT_STATUS_CHOICES,
        default='none',
        blank=True,
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    confirmation_email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.invention_title} by {self.inventor_name}"


