from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
import datetime

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
    # Birthday fields as separate dropdowns
    birth_month = forms.ChoiceField(
        choices=[(str(i), datetime.date(1900, i, 1).strftime('%B')) for i in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={'class': 'birth-month'})
    )
    birth_day = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 32)],
        required=False,
        widget=forms.Select(attrs={'class': 'birth-day'})
    )
    birth_year = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(datetime.datetime.now().year, 1899, -1)],
        required=False,
        widget=forms.Select(attrs={'class': 'birth-year'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'country', 'state', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email field unique but allow current user's email
        self.fields['email'].required = True

        # Set initial values for birthday fields if birthday exists
        if self.instance and self.instance.birthday:
            self.fields['birth_month'].initial = str(self.instance.birthday.month)
            self.fields['birth_day'].initial = str(self.instance.birthday.day)
            self.fields['birth_year'].initial = str(self.instance.birthday.year)

    def clean(self):
        cleaned_data = super().clean()
        birth_month = cleaned_data.get('birth_month')
        birth_day = cleaned_data.get('birth_day')
        birth_year = cleaned_data.get('birth_year')

        # Combine birthday fields into a single date
        if birth_year and birth_month and birth_day:
            try:
                birthday = datetime.date(int(birth_year), int(birth_month), int(birth_day))
                cleaned_data['birthday'] = birthday
            except ValueError:
                raise forms.ValidationError("Invalid date selected.")
        elif birth_year or birth_month or birth_day:
            # If any birthday field is filled, all must be filled
            raise forms.ValidationError("Please provide complete birthday information or leave all fields empty.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
