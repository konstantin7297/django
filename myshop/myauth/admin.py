from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile
from .forms import ProfileForm


class UserInline(admin.TabularInline):
    model = Profile


class CustomUserAdmin(UserAdmin):
    inlines = [UserInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    add_form = ProfileForm
    list_display = ("user", "fullName", "email", "phone")
    list_display_links = ("fullName",)
    ordering = ("pk", "fullName")
    search_fields = ("fullName", "email", "phone")
    fieldsets = [
        ("Profile", {
            "description": "Profile information",
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
