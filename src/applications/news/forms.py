from typing import Any

from django import forms

from .models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "text", "image", "publish"]
