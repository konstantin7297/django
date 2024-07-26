from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "image")
    list_display_links = ("title",)
    ordering = ("title",)
    search_fields = ("title",)
    fieldsets = [
        (None, {
            "description": "Main information of the category",
            "fields": ("title",),
        }),
        ("image", {
            "description": "Image of the category",
            "fields": ("image",),
            "classes": ("collapse",),
        }),
        ("Subcategories", {
            "description": "Subcategories of the category",
            "fields": ("subcategories",),
            "classes": ("collapse",),
        }),
    ]

    def get_queryset(self, request):
        return Category.objects.prefetch_related("subcategories")


# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ("number", "name", "month", "year", "code")
#     list_display_links = ("number", "name")
#     ordering = ("number", "name")
#     search_fields = ("number", "name")
#     fieldsets = [
#         ("Payment", {
#             "description": "Payment information",
#             "fields": ("number", "name", "month", "year", "code"),
#         })
#     ]
