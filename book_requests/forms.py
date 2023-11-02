from captcha.fields import CaptchaField
from django import forms


class BookRequestForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Write comment", "size": 5})
    )
    captcha = CaptchaField()
