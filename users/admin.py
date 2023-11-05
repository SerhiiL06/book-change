from django.contrib import admin
from .models import User, UserFollowing, UserProfile


# @admin.action(description="Set active status")
# def set_unactive(modeladmin, request, queryset):
#     queryset.update(is_active=False)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "last_activity", "full_name"]

    list_display_links = ["full_name"]
    actions = ["set_active", "set_unactive"]
    date_hierarchy = "join_at"
    empty_value_display = "--"

    @admin.action(description="Set active status")
    def set_active(self, request, queryset):
        unactive = queryset.filter(is_active=False).count()
        queryset.update(is_active=True)
        self.message_user(request, f"You're update {unactive} user")

    @admin.action(description="Unset active status")
    def set_unactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"You're update {queryset.count()} user")


@admin.register(UserFollowing)
class FollowingAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
