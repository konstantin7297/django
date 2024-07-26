from django.contrib import admin

from .models import Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image")
    list_display_links = ("id", "title",)
    ordering = ("id", "title",)
    search_fields = ("title",)
    verbose_name = "Category"
    verbose_name_plural = "Categories"
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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_display_links = ("id", "name")
    ordering = ("id", "name")
    search_fields = ("name",)
    fieldsets = [
        (None, {
            "description": "Main information of the tag",
            "fields": ("name",),
        }),
        ("Category", {
            "description": "Category of the tag",
            "fields": ("category",),
            "classes": ("collapse",),
        }),
    ]

    def get_queryset(self, request):
        return Tag.objects.select_related("category")


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
