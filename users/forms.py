from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Interest

class RegisterForm(UserCreationForm):
    """
    A form for user registration.
    """

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username

class LoginForm(AuthenticationForm):
    """
    A form for user login.
    """
    class Meta:
        model = User
        fields = ['username', 'password']

class InterestForm(forms.ModelForm):
    """
    A form for creating and editing Interest objects.
    """

    class Meta:
        model = Interest
        fields = ['message']
        