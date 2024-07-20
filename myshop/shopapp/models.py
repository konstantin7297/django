from django.db import models
from django.utils import timezone
import zoneinfo

tz = zoneinfo.ZoneInfo('Europe/Berlin')
timezone.activate(tz)


def path_to_category_img(instance: "Category", filename: str) -> str:
    return f"categories/category_{instance.pk}/image/{filename}"


def path_to_product_img(instance: "Product", filename: str) -> str:
    return f"products/product_{instance.pk}/image/{filename}"


class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=path_to_category_img)
    subcategories = models.ManyToManyField("self")

    def __str__(self) -> str:
        return f"Category: {self.title!r}"


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"Tag: {self.name!r}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    freeDelivery = models.BooleanField(default=False)
    reviews = models.PositiveIntegerField(default=0)
    rating = models.FloatField(null=True, default=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name="products")

    def __str__(self) -> str:
        return f"Product: {self.title!r}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=path_to_product_img)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    deliveryType = models.CharField(max_length=50)
    paymentType = models.CharField(max_length=50)
    totalCost = models.FloatField(default=0)
    status = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, related_name="orders")

    def __str__(self) -> str:
        return f"Order: {self.fullName!r}"
