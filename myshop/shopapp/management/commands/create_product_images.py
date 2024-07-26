from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Product, ProductImage


class Command(BaseCommand):
    """ Command for creating product images """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating product images")
        count: int = 10

        products = Product.objects.all()
        product_images = [
            ProductImage(product=products[i - 1], image="my_img.jpg")
            for i in range(1, count)
        ]
        ProductImage.objects.bulk_create(product_images)

        self.stdout.write(self.style.SUCCESS(f"{count - 1} product images created"))
