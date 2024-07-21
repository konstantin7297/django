import random

from django.core.management import BaseCommand

from shopapp.models import Product, Category


class Command(BaseCommand):
    """ Command for creating products """
    def handle(self, *args, **options):
        self.stdout.write("Creating products")
        products = [Product(
            category=Category.objects.get(id=i),
            price=round(random.uniform(1000, 5000), 2),
            count=random.randint(10, 100),
            title=f"Product{i}",
            description=f"Description{i}",
            freeDelivery=random.choice([True, False]),
        ) for i in range(1, 10)]

        Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS(
            f"Creating {len(products)} products is done"
        ))
