from typing import Any
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        help_text="Your password can’t be too similar to your other personal information.",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )

    class Meta:
        model = User
        fields = ["email", "password"]
