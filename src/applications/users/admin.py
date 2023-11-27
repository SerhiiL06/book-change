from django.contrib import admin
from src.applications.books.inlines import BookInline

from .models import User, UserEmailNewsLetter, UserFollowing, UserProfile
from .inlines import UserFollowingInlines, NewsLetterSettingsInline


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "is_active",
        "full_name",
    ]
    list_display_links = ["email"]

    fields = [
        "email",
        ("first_name", "last_name"),
        "join_at",
        "last_activity",
        ("is_staff", "is_superuser"),
        "is_active",
        "groups",
    ]

    list_filter = ["is_active"]
    search_fields = ["email", "first_name"]
    ordering = ["email"]
    actions = ["set_active", "set_unactive"]
    readonly_fields = ["email", "last_activity", "join_at", "status"]
    inlines = [BookInline, NewsLetterSettingsInline, UserFollowingInlines]

    @admin.action(description="Set active status")
    def set_active(self, request, queryset):
        unactive = queryset.filter(is_active=False).count()
        queryset.update(is_active=True)
        self.message_user(request, f"You're update {unactive} user")

    @admin.action(description="Unset active status")
    def set_unactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"You're update {queryset.count()} user")


@admin.register(UserFollowing)
class FollowingAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserEmailNewsLetter)
