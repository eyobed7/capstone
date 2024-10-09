# Django imports
from django import forms  # For creating and handling forms
from django.contrib.auth.models import User  # Default user model in Django
from django.core.exceptions import ValidationError  # For handling validation errors in forms


# Form widgets for customizing input fields
from django.forms.widgets import PasswordInput, TextInput, EmailInput  # Custom widgets for form inputs

# Django's built-in authentication form
from django.contrib.auth.forms import AuthenticationForm  # Default form for handling user authentication


User=get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")

class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
        # Override the default username field to remove it
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')  # Remove the username field
