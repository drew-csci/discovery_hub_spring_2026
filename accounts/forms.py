from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
import datetime

US_STATES = [
    ('Alabama', 'Alabama'),
    ('Alaska', 'Alaska'),
    ('Arizona', 'Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('Delaware', 'Delaware'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oklahoma', 'Oklahoma'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming'),
]

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
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'country', 'state', 'city', 'zip_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email field unique but allow current user's email
        self.fields['email'].required = True
        
        # Set country default to United States
        self.fields['country'].initial = 'United States'
        
        # Update state field with US states
        self.fields['state'].widget = forms.Select(choices=[('', 'Select State')] + US_STATES)
        self.fields['state'].label = 'State'
        
        # Change city to text input
        self.fields['city'].widget = forms.TextInput(attrs={'placeholder': 'Enter your city'})
        
        # Add zip code field with validation
        self.fields['zip_code'].widget = forms.TextInput(attrs={'placeholder': '12345', 'pattern': '[0-9]{5}', 'maxlength': '5'})
        self.fields['zip_code'].label = 'ZIP Code'

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

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if zip_code and not zip_code.isdigit():
            raise forms.ValidationError('ZIP Code must contain only numbers.')
        if zip_code and len(zip_code) != 5:
            raise forms.ValidationError('ZIP Code must be exactly 5 digits.')
        return zip_code
