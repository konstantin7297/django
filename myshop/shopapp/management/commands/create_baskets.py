from random import randint, choice

from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Basket, Product


class Command(BaseCommand):
    """ Command for creating baskets """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating baskets")
        count: int = 10

        products = Product.objects.all()
        baskets = [
            Basket(user=i, count=randint(1, 5), product=choice(products))
            for i in range(1, count)
        ]
        Basket.objects.bulk_create(baskets)

        self.stdout.write(self.style.SUCCESS(f"{count - 1} baskets created"))
