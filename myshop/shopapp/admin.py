from django.contrib import admin

from .models import (
    Category,
    Tag,
    Product,
    ProductImage,
    Specification,
    Review,
    Basket,
    Order,
    Payment,
    Sale,
    SaleImage,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image")
    list_display_links = ("id", "title",)
    ordering = ("id", "title",)
    search_fields = ("title",)
    verbose_name_plural = "Categories"
    fieldsets = [
        (None, {
            "description": "Main information of the category",
            "fields": ("title",),
        }),
        ("Relationships", {
            "description": "Relationships information of the category",
            "fields": ("image", "subcategories"),
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
        ("Relationships", {
            "description": "Relationships information of the tag",
            "fields": ("category",),
            "classes": ("collapse",),
        }),
    ]

    def get_queryset(self, request):
        return Tag.objects.select_related("category")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "price", "count", "description", "freeDelivery", "limited",
        "date"
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
            "fields": ("price", "count", "rating"),
        }),
        ("Relationships", {
            "description": "Relationships information of the product",
            "fields": ("category", "tags"),
            "classes": ("collapse",),
        }),
    ]

    def get_queryset(self, request):
        return (
            Product.objects
            .select_related("category")
            .prefetch_related("tags")
            .filter(sale=False)
        )


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
        }),
    ]

    def get_queryset(self, request):
        return ProductImage.objects.select_related("product")


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "name", "value")
    list_display_links = ("id", "product", "name", "value")
    ordering = ("id", "product", "name")
    search_fields = ("id", "product", "name", "value")
    fieldsets = [
        (None, {
            "description": "Main information of the product specification",
            "fields": ("product", "name", "value"),
        }),
    ]

    def get_queryset(self, request):
        return Specification.objects.select_related("product")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "email", "text", "rate", "product", "date")
    list_display_links = ("id", "author", "email")
    ordering = ("id", "date")
    search_fields = ("id", "author", "email", "text", "rate")
    fieldsets = [
        (None, {
            "description": "Main information of the product review",
            "fields": ("product", "author", "email", "text", "rate"),
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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "fullName", "email", "phone", "deliveryType", "paymentType", "totalCost",
        "status", "createdAt"
    )
    list_display_links = ("id", "fullName", "email", "phone")
    ordering = ("id", "createdAt")
    search_fields = ("id", "fullName", "email", "phone", "totalCost")
    fieldsets = [
        (None, {
            "description": "Main information of the order",
            "fields": (
                "fullName", "email", "phone", "deliveryType", "paymentType",
                "totalCost", "status", "city", "address"
            ),
        }),
        ("Relationships", {
            "description": "Relationships information of the order",
            "fields": ("products",),
            "classes": ("collapse",),
        }),
    ]

    def get_queryset(self, request):
        return Order.objects.prefetch_related("products")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "name", "month", "year", "code", "order")
    list_display_links = ("id", "number", "name")
    ordering = ("id", "number", "name")
    search_fields = ("number", "name", "month", "year")
    fieldsets = [
        (None, {
            "description": "Payment information",
            "fields": ("number", "name", "month", "year", "code", "order"),
        }),
    ]

    def get_queryset(self, request):
        return Payment.objects.select_related("order")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "salePrice", "dateFrom", "dateTo")
    list_display_links = ("id", "title")
    ordering = ("id", "dateFrom", "dateTo")
    search_fields = ("id", "title", "price", "salePrice")
    fieldsets = [
        (None, {
            "description": "Main information of the sale",
            "fields": ("title", "price", "salePrice"),
        }),
    ]


@admin.register(SaleImage)
class SaleImageAdmin(admin.ModelAdmin):
    list_display = ("id", "sale", "image")
    list_display_links = ("id", "sale")
    ordering = ("id", "sale")
    search_fields = ("id", "sale")
    fieldsets = [
        (None, {
            "description": "Main information of the sale image",
            "fields": ("sale", "image"),
        }),
    ]

    def get_queryset(self, request):
        return SaleImage.objects.select_related("sale")
