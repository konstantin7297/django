from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def path_to_img(instance, filename: str) -> str:
    """ Function for create path to save images """
    cls_name = instance.__class__.__name__.lower()
    return f"{cls_name}/id_{instance.pk}/images/{filename}"


class Category(models.Model):
    """ Model for categories """
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to=path_to_img)
    subcategories = models.ManyToManyField("self")

    def __str__(self) -> str:
        return f"Category: {self.title!r}"


class Tag(models.Model):
    """ Model for tags """
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tags"
    )
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"Tag: {self.name!r}"


class Product(models.Model):
    """ Model for products """
    class Meta:
        ordering = ['price']

    price = models.DecimalField(max_digits=50, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True, blank=True)
    fullDescription = models.TextField(max_length=500, null=True, blank=True)
    freeDelivery = models.BooleanField(default=False)
    rating = models.FloatField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(5)
    ])
    limited = models.BooleanField(default=False)
    sale = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    tags = models.ManyToManyField(Tag, related_name="products")

    def __str__(self) -> str:
        return f"Product: {self.title!r}"


class ProductImage(models.Model):
    """ Model for product images """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=path_to_img)


class Specification(models.Model):
    """ Model for product specifications """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)


class Review(models.Model):
    """ Model for product reviews """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    author = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    text = models.CharField(max_length=500)
    rate = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(5)
    ])
    date = models.DateTimeField(auto_now_add=True)


class Basket(models.Model):
    """ Model for baskets """
    user = models.PositiveBigIntegerField()
    count = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="baskets"
    )

    def __str__(self) -> str:
        return f"Basket: {self.user!r}"


class Order(models.Model):
    """ Model for orders """
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    deliveryType = models.CharField(max_length=99, choices=[
        ("ordinary", "free"), ("express", "paying"),
    ])
    paymentType = models.CharField(max_length=99, choices=[
        ("online", "card"), ("someone", "cash"),
    ])
    totalCost = models.DecimalField(default=0, max_digits=50, decimal_places=2)
    status = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, related_name="orders")

    def __str__(self) -> str:
        return f"Order: {self.fullName!r}"


class Payment(models.Model):
    """ Model for payments """
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name="payments")
    number = models.PositiveBigIntegerField(validators=[
        MinValueValidator(1000000000000000), MaxValueValidator(9999999999999999)
    ], unique=True)
    name = models.CharField(max_length=50)
    month = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(12)
    ])
    year = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(datetime.now().year),
        MaxValueValidator(datetime.now().year + 3),
    ])
    code = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(100), MaxValueValidator(999)
    ])


class Sale(models.Model):
    """ Model for sales """
    price = models.DecimalField(max_digits=50, decimal_places=2)
    salePrice = models.DecimalField(max_digits=50, decimal_places=2)
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"Sale: {self.title!r}"


class SaleImage(models.Model):
    """ Model for sale images """
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=path_to_img)
