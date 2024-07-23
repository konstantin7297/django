from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, Payment


class UserInline(admin.TabularInline):
    model = Profile


class CustomUserAdmin(UserAdmin):
    inlines = [UserInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
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


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "month", "year", "code")
    list_display_links = ("number", "name")
    ordering = ("number", "name")
    search_fields = ("number", "name")
    fieldsets = [
        ("Payment", {
            "description": "Payment information",
            "fields": ("number", "name", "month", "year", "code"),
        })
    ]
