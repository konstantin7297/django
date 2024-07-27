from django.contrib import admin

from .models import Category, Tag, Product, ProductImage, Specification, Review, Basket


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "price", "count", "description", "freeDelivery", "limited"
    )
    list_display_links = ("id", "title", "description")
    ordering = ("id", "title")
    search_fields = ("title", "description", "price", "count")
    fieldsets = [
        (None, {
            "description": "Main information of the product",
            "fields": (
                "title", "description", "fullDescription", "freeDelivery", "limited"
            ),
        }),
        ("Integers", {
            "description": "Side information of the product",
            "fields": ("price", "count", "date", "rating"),
        }),
        ("Relationships", {
            "description": "Relationships information of the product",
            "fields": ("category", "tags"),
            "classes": ("collapse",),
        }),
    ]

    def get_queryset(self, request):  # TODO: images, specifications, reviews, baskets
        return Product.objects.select_related("category").prefetch_related("tags")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "image")
    list_display_links = ("id", "product")
    ordering = ("id", "product")
    search_fields = ("id", "product")
    fieldsets = [
        (None, {
            "description": "Main information of the product image",
            "fields": ("product", "image"),
        })
    ]

    def get_queryset(self, request):
        return ProductImage.objects.select_related("product")


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "name", "value")
    list_display_links = ("id", "product", "name")
    ordering = ("id", "product", "name")
    search_fields = ("id", "product", "name", "value")
    fieldsets = [
        (None, {
            "description": "Main information of the product specification",
            "fields": ("product", "name", "value"),
        })
    ]

    def get_queryset(self, request):
        return Specification.objects.select_related("product")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "author", "email", "text", "rate")
    list_display_links = ("id", "product", "author", "email")
    ordering = ("id", "product")
    search_fields = ("id", "product", "author", "email", "text")
    fieldsets = [
        (None, {
            "description": "Main information of the product review",
            "fields": ("product", "author", "email", "text", "rate", "date"),
        })
    ]

    def get_queryset(self, request):
        return Review.objects.select_related("product")


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "count", "product")
    list_display_links = ("id", "user", "count")
    ordering = ("id", "user", "count")
    search_fields = ("id", "user", "count", "product")
    fieldsets = [
        (None, {
            "description": "Main information of the basket",
            "fields": ("user", "count", "product"),
        }),
    ]

    def get_queryset(self, request):
        return Basket.objects.select_related("product")


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
