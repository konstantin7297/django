import random

from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Product, Category, Tag, ProductImage, Specification, Review


class Command(BaseCommand):
    """ Command for creating products """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating products")
        categories = Category.objects.all()
        tags = Tag.objects.all()
        products = [
            Product(
                category=random.choice(categories),
                price=round(random.uniform(1000, 5000), 2),
                count=random.randint(10, 100),
                title=f"Product{i}",
                description=f"Description{i}",
                fullDescription=f"fullDescription{i}",
                freeDelivery=random.choice([True, False]),
            ) for i in range(1, 10)
        ]
        Product.objects.bulk_create(products)

        products = Product.objects.all()
        for product in products:
            product.tags.add(random.choice(tags))
            product.save()

        product_images = [
            ProductImage(
                product=random.choice(products),
                image="/uploads/my_img.jpg"
            ) for _ in range(1, 10)
        ]
        ProductImage.objects.bulk_create(product_images)
        specifications = [
            Specification(
                product=random.choice(products),
                name=f"name{i}",
                value=f"value{i}"
            )
            for i in range(1, 10)
        ]
        Specification.objects.bulk_create(specifications)
        reviews = [
            Review(
                product=random.choice(products),
                author=f"author{i}",
                email=f"khromykh.kas{i}@mail.ru",
                text=f"text{i}",
                rate=random.randint(1, 5),
            )
            for i in range(1, 10)
        ]
        Review.objects.bulk_create(reviews)
        self.stdout.write(self.style.SUCCESS(
            f"Creating {len(products)} products is done"
        ))
