from django.contrib import admin

from .models import UserEmailNewsLetter, UserFollowing


class UserFollowingInlines(admin.TabularInline):
    model = UserFollowing
    verbose_name_plural = "followers"
    fk_name = "user_id"
    extra = 0
    readonly_fields = ["followers_id"]


class NewsLetterSettingsInline(admin.TabularInline):
    model = UserEmailNewsLetter
    extra = 0
