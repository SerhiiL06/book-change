from django import forms
from django.db.models import Q

from src.applications.users.models import User, UserFollowing


class ShareMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    def __init__(self, data, user=None):
        super().__init__(data)
        ids = UserFollowing.objects.values_list("user_id").filter(followers_id=user)
        self.fields["recipient"].queryset = User.objects.filter(id__in=ids)
