from random import uniform, randint, choice

from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Tag, Category, Product, ProductImage, Review, Specification


class Command(BaseCommand):
    """ Command for creating products """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating products")
        count: int = 100

        categories = Category.objects.all()
        products = [Product(
            price=round(uniform(1, 50000), 2),
            count=randint(10, 100),
            title=f"product{i}",
            description=f"description{i}",
            fullDescription=f"fullDescription{i}",
            freeDelivery=choice([True, False]),
            limited=choice([True, False]),
            category=categories[i - 1],
        ) for i in range(1, count)]
        products = Product.objects.bulk_create(products)

        tags = Tag.objects.all()
        for product in products:
            product.tags.add(choice(tags))
            product.save()

        images = [
            ProductImage(product=products[i - 1], image="my_img.jpg")
            for i in range(1, count)
        ]

        reviews = [Review(
            product=products[i - 1],
            author=f"review{i}",
            email=f"review{i}@mail.ru",
            text=f"text{i}",
            rate=randint(1, 5),
        ) for i in range(1, count)]

        specifications = [
            Specification(product=products[i - 1], name=f"name{i}", value=f"value{i}")
            for i in range(1, count)
        ]

        ProductImage.objects.bulk_create(images)
        Review.objects.bulk_create(reviews)
        Specification.objects.bulk_create(specifications)

        self.stdout.write(self.style.SUCCESS(f"{count - 1} products created"))
