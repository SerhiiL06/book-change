from typing import Any
from django import forms
from .models import ImageTag, Gallery


class UploadImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Gallery
        fields = ["image", "tags"]
