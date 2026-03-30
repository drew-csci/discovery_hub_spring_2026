from django.db import models
from django.conf import settings


class Post(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    organization_name = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=50)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media = models.FileField(upload_to='post_media/', blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MediaType.choices, default=MediaType.IMAGE, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.organization_name}"

    def save(self, *args, **kwargs):
        if self.media and not self.media_type:
            name = self.media.name.lower()
            if name.endswith(('.mp4', '.avi', '.mov', '.webm')):
                self.media_type = self.MediaType.VIDEO
            else:
                self.media_type = self.MediaType.IMAGE

        if not self.organization_name and self.author:
            # Only auto-populate if user has set a proper display name (not just email)
            display_name = self.author.display_name
            if display_name and display_name != self.author.email:
                self.organization_name = display_name
                self.organization_type = self.author.user_type
            else:
                # For new users without profile info, leave organization_name empty
                # and set organization_type to user's type
                self.organization_type = self.author.user_type

        super().save(*args, **kwargs)
