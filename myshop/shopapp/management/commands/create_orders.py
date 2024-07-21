import random

from django.core.management import BaseCommand

from shopapp.models import Order


class Command(BaseCommand):
    """ Command for creating orders """
    def handle(self, *args, **options):
        self.stdout.write("Creating orders")
        orders = [Order(
            fullName=f"Order{i}",
            email=f"myemail{i}@mail.ru",
            phone=f"8904571224{i}",
            deliveryType=f"deliveryType{i}",
            paymentType=f"paymentType{i}",
            totalCost=round(random.uniform(10, 100), 2),
            status=f"status{i}",
            city=f"city1",
            address=f"address1",
        ) for i in range(1, 10)]

        Order.objects.bulk_create(orders)

        self.stdout.write(self.style.SUCCESS(
            f"Creating {len(orders)} orders is done"
        ))
