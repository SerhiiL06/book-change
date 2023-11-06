from typing import Any

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField

from .models import User, UserEmailNewsLetter, UserProfile


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


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"readonly": True}))
    first_name = forms.CharField()
    last_name = forms.CharField()
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    about = forms.CharField(widget=forms.Textarea(attrs={"size": 15}))

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "image", "about"]


class OptionalUserInformationForm(forms.ModelForm):
    country = CountryField(blank_label="{select country}")
    phone_number = PhoneNumberField(region="UA", required=False)
    social_link = forms.URLField(widget=forms.URLInput, required=False)

    class Meta:
        model = UserProfile
        fields = ["phone_number", "country", "social_link", "profession", "social_link"]


class MessageForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Subject"}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Your message"})
    )
    captcha = CaptchaField()

    def clean_field(self):
        subject = self.cleaned_data["subject"]
        message = self.cleaned_data["message"]
        data = {"subject": subject, "message": message}
        return data


class EmailNewsLetterForm(forms.ModelForm):
    class Meta:
        model = UserEmailNewsLetter
        fields = ["sending_out_offers", "news_mailer"]
