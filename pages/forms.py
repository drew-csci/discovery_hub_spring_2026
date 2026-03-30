from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'media']

    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media:
            if media.size > 20 * 1024 * 1024:
                raise forms.ValidationError('Media file must be below 20MB.')
            content_type = media.content_type
            if not any(x in content_type for x in ['image/', 'video/']):
                raise forms.ValidationError('Only image or video files are allowed.')
        return media
