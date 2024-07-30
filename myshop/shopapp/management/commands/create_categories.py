from random import choice

from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Category


class Command(BaseCommand):
    """ Command for creating categories """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating categories")
        count: int = 100

        categories = [
            Category(title=f"category{i}", image="my_img.jpg") for i in range(1, count)
        ]
        Category.objects.bulk_create(categories)
        categories = Category.objects.all()

        for cat in categories:
            cat.subcategories.add(choice(
                [category for category in categories if cat != category]
            ))
            cat.save()

        self.stdout.write(self.style.SUCCESS(f"{count - 1} categories created"))
