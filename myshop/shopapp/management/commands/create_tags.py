from django.core.management import BaseCommand

from shopapp.models import Tag


class Command(BaseCommand):
    """ Command for creating tags """
    def handle(self, *args, **options):
        self.stdout.write("Creating tags")
        tags = [Tag(name=f"Tag{i}") for i in range(1, 10)]
        Tag.objects.bulk_create(tags)

        self.stdout.write(self.style.SUCCESS(
            f"Creating {len(tags)} tags is done"
        ))
