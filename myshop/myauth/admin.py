from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile


class UserInline(admin.TabularInline):
    model = Profile


class CustomUserAdmin(UserAdmin):
    inlines = [UserInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "fullName", "email", "phone")
    list_display_links = ("id", "fullName",)
    ordering = ("id", "fullName")
    search_fields = ("fullName", "email", "phone")
    fieldsets = [
        (None, {
            "description": "Main profile information",
            "fields": ("user", "fullName", "email", "phone"),
        }),
        ("Media", {
            "description": "Block for media files",
            "fields": ("avatar",),
            "classes": ("collapse",),
        })
    ]

    def get_queryset(self, request):
        return Profile.objects.select_related("user")
