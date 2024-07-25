import random

from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Tag, Category


class Command(BaseCommand):
    """ Command for creating tags """

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating tags")
        categories = Category.objects.all()
        tags = [
            Tag(category=random.choice(categories), name=f"tag{i}")
            for i in range(1, 10)
        ]
        Tag.objects.bulk_create(tags)
        self.stdout.write(self.style.SUCCESS(
            f"Creating {len(tags)} tags is done"
        ))
