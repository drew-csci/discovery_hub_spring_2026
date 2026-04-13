from datetime import date

from django import forms

from .models import InventionDisclosure


class InventionDisclosureForm(forms.ModelForm):
    class Meta:
        model = InventionDisclosure
        fields = [
            'inventor_name',
            'inventor_email',
            'invention_title',
            'invention_description',
            'technology_field',
            'date_of_invention',
            'inventors',
            'patent_status',
        ]
        widgets = {
            'inventor_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your full name'}
            ),
            'inventor_email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'name@example.com'}
            ),
            'invention_title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Title of your invention'}
            ),
            'invention_description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe the invention in detail...'}
            ),
            'technology_field': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'e.g. Biotech, AI, Materials'}
            ),
            'date_of_invention': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'inventors': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'List other inventors if applicable (optional)',
                }
            ),
            'patent_status': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'inventor_name': 'Inventor Name *',
            'inventor_email': 'Email Address *',
            'invention_title': 'Title of Invention *',
            'invention_description': 'Description *',
            'technology_field': 'Technology Field',
            'date_of_invention': 'Date of Invention',
            'inventors': 'Other Inventors',
            'patent_status': 'Patent Status',
        }
        help_texts = {
            'inventor_email': 'A confirmation message will be sent to this email address.',
            'inventors': 'Optional: enter any additional contributors or co-inventors.',
        }
        error_messages = {
            'inventor_name': {
                'required': 'Inventor name is required.',
                'max_length': 'Inventor name must be 255 characters or less.',
            },
            'inventor_email': {
                'required': 'Email address is required.',
                'invalid': 'Enter a valid email address.',
            },
            'invention_title': {
                'required': 'Invention title is required.',
                'max_length': 'Title must be 255 characters or less.',
            },
            'invention_description': {
                'required': 'Description is required.',
            },
        }

    def clean_inventor_name(self):
        name = self.cleaned_data.get('inventor_name', '').strip()
        if not name:
            raise forms.ValidationError('Inventor name is required.')
        if len(name) < 2:
            raise forms.ValidationError('Inventor name must be at least 2 characters.')
        return name

    def clean_inventor_email(self):
        email = self.cleaned_data.get('inventor_email', '').strip()
        if not email:
            raise forms.ValidationError('Email address is required.')
        return email

    def clean_invention_description(self):
        description = self.cleaned_data.get('invention_description', '').strip()
        if not description:
            raise forms.ValidationError('Description is required.')
        if len(description) < 10:
            raise forms.ValidationError('Description must be at least 10 characters.')
        return description

    def clean_date_of_invention(self):
        invention_date = self.cleaned_data.get('date_of_invention')
        if invention_date and invention_date > date.today():
            raise forms.ValidationError('Date of invention cannot be in the future.')
        return invention_date
