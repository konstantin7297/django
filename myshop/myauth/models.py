from django.contrib.auth.models import User
from django.db import models


def path_to_avatar(instance: "Profile", filename: str) -> str:
    return f"profiles/profile_{instance.pk}/avatar/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=path_to_avatar)
