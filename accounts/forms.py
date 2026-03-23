from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.UserType.choices, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'user_type')

class EmailAuthenticationForm(AuthenticationForm):
    # Field is still named "username" internally; label it clearly as Email.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update({'placeholder': 'you@example.com', 'autofocus': True})
        self.fields['password'].widget.attrs.update({'placeholder': 'password'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email field unique but allow current user's email
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
