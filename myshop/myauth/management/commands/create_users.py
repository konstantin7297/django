from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from myauth.models import Profile


class Command(BaseCommand):
    """ Command for creating users and users profile """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating users")
        count: int = 10

        users = [
            User(
                first_name=f"first_name{i}",
                username=f"username{i}",
                password=make_password(f"password{i}"),
            ) for i in range(1, count)
        ]
        User.objects.bulk_create(users)

        profiles = [
            Profile(
                user=users[i - 1],
                fullName=f"fullName{i}",
                email=f"email{i}@mail.ru",
                phone=88009991120 + i,
                avatar="my_img.jpg",
            ) for i in range(1, count)
        ]
        Profile.objects.bulk_create(profiles)

        self.stdout.write(self.style.SUCCESS(f"{count - 1} users created"))
