from random import uniform, randint, choice

from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Tag, Category, Product


class Command(BaseCommand):
    """ Command for creating products """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating products")
        count: int = 10

        categories = Category.objects.all()
        products = [
            Product(
                price=round(uniform(1000, 10000), 2),
                count=randint(10, 100),
                title=f"product{i}",
                description=f"description{i}",
                fullDescription=f"fullDescription{i}",
                freeDelivery=choice([True, False]),
                limited=choice([True, False]),
                category=categories[i - 1],
            ) for i in range(1, count)
        ]
        Product.objects.bulk_create(products)

        tags = Tag.objects.all()
        products = Product.objects.all()
        for product in products:
            product.tags.add(choice(tags))
            product.save()

        self.stdout.write(self.style.SUCCESS(f"{count - 1} products created"))
