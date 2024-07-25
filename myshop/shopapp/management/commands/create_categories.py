from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Category


class Command(BaseCommand):
    """ Command for creating categories """

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating categories")
        categories = [
            Category(title=f"Category{i}", image="/uploads/my_img.jpg")
            for i in range(1, 10)
        ]
        Category.objects.bulk_create(categories)
        self.stdout.write(self.style.SUCCESS(
            f"Creating {len(categories)} categories is done"
        ))
