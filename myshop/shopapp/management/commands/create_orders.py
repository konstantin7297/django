from random import choice

from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import F

from shopapp.models import Order, Product


class Command(BaseCommand):
    """ Command for creating orders """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating orders")
        count: int = 10

        orders = [
            Order(
                fullName=f"fullName{i}",
                email=f"order{i}@mail.ru",
                phone=f"8900555353{i}",
                deliveryType=choice(["Delivery", "ExpressDelivery"]),
                paymentType=choice(["CardOnline", "AlienOnline"]),
                status=choice(["accepted", "denied"]),
                city=f"city{i}",
                address=f"address{i}",
            ) for i in range(1, 10)
        ]
        Order.objects.bulk_create(orders)

        products = Product.objects.all()
        for order in Order.objects.all():
            product = choice(products)
            order.products.add(product)
            order.totalCost = F("totalCost") + product.price

        self.stdout.write(self.style.SUCCESS(f"{count - 1} orders created"))
