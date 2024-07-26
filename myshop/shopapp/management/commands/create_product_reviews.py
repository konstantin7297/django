from random import *

from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Product, Review


class Command(BaseCommand):
    """ Command for creating product reviews """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating product reviews")
        count: int = 10

        products = Product.objects.all()
        reviews = [
            Review(
                product=products[i - 1],
                author=f"review{i}",
                email=f"review{i}@mail.ru",
                text=f"text{i}",
                rate=randint(1, 5),
            ) for i in range(1, count)
        ]
        Review.objects.bulk_create(reviews)

        self.stdout.write(self.style.SUCCESS(f"{count - 1} product reviews created"))
