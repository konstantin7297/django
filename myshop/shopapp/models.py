from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
import zoneinfo

tz = zoneinfo.ZoneInfo('Europe/Berlin')
timezone.activate(tz)


def path_to_img(instance, filename: str) -> str:
    """ Function for create path to save images """
    cls_name = instance.__class__.__name__.lower()
    return f"{cls_name}/id_{instance.pk}/images/{filename}"


class Category(models.Model):
    """ Model for categories """
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to=path_to_img)
    subcategories = models.ManyToManyField("self")

    def __str__(self) -> str:
        return f"Category: {self.title!r}"


class Tag(models.Model):
    """ Model for tags """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"Tag: {self.name!r}"


class Product(models.Model):
    """ Model for products """
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(max_digits=50, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True, blank=True)
    fullDescription = models.TextField(max_length=500, null=True, blank=True)
    freeDelivery = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="products")
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    limited = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Product: {self.title!r}"


class ProductImage(models.Model):
    """ Model for product images """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=path_to_img)


class Review(models.Model):
    """ Model for product reviews """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    text = models.CharField(max_length=500)
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(default=timezone.now)


class Specification(models.Model):
    """ Model for product specifications """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)


class Order(models.Model):
    """ Model for orders """
    createdAt = models.DateTimeField(default=timezone.now)
    fullName = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    deliveryType = models.CharField(max_length=50, choices=[
        ("Del", "Доставка"), ("ExDel", "Экспресс-доставка")
    ])
    paymentType = models.CharField(max_length=50, choices=[
        ("Online", "Онлайн картой"), ("Alien Online", "Онлайн со случайного чужого счёта")
    ])
    totalCost = models.FloatField(default=0)
    status = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, related_name="orders")

    def __str__(self) -> str:
        return f"Order: {self.fullName!r}"


# class Sales(models.Model):
#     price = models.DecimalField(max_digits=50, decimal_places=2)
#     salePrice = models.DecimalField(max_digits=50, decimal_places=2)
#     dateFrom = models.DateTimeField(auto_now_add=True)
#     dateTo = models.DateTimeField()
#     title = models.CharField(max_length=50)


# class SalesImage(models.Model):
#     sales = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name="images")
#     image = models.ImageField(upload_to=path_to_img)
