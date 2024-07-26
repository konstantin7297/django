from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Product, Specification


class Command(BaseCommand):
    """ Command for creating product specifications """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating product specifications")
        count: int = 10

        products = Product.objects.all()
        product_specifications = [
            Specification(product=products[i - 1], name=f"name{i}", value=f"value{i}")
            for i in range(1, count)
        ]
        Specification.objects.bulk_create(product_specifications)

        self.stdout.write(
            self.style.SUCCESS(f"{count - 1} product specifications created")
        )
