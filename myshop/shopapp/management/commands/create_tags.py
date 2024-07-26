from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Tag, Category


class Command(BaseCommand):
    """ Command for creating tags """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating tags")
        count: int = 10

        categories = Category.objects.all()
        tags = [
            Tag(category=categories[i - 1], name=f"tag{i}")
            for i in range(1, count)
        ]
        Tag.objects.bulk_create(tags)

        self.stdout.write(self.style.SUCCESS(f"{count - 1} tags created"))
