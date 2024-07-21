from django.core.management import BaseCommand

from shopapp.models import Category


class Command(BaseCommand):
    """ Command for creating categories """
    def handle(self, *args, **options):
        self.stdout.write("Creating categories")
        categories = [Category(title=f"Category{i}") for i in range(1, 10)]
        Category.objects.bulk_create(categories)

        self.stdout.write(self.style.SUCCESS(
            f"Creating {len(categories)} categories is done"
        ))
