from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]
