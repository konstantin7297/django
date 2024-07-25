import random

from django.core.management import BaseCommand

from shopapp.models import Product, Order


class Command(BaseCommand):
    """ Command for updating products """
    def handle(self, *args, **options):
        self.stdout.write("Updating products")
        products = Product.objects.all()
        orders = Order.objects.all()

        for product in products:
            product.tags.add(random.randint(1, 9))
            product.orders.add(random.choice(orders))
            product.save()

        self.stdout.write(self.style.SUCCESS(
            f"Updating {len(products)} products is done"
        ))
