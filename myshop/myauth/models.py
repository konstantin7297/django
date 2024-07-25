from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def path_to_img(instance, filename: str) -> str:
    """ Function for create path to save images """
    cls_name = instance.__class__.__name__.lower()
    return f"{cls_name}/id_{instance.pk}/images/{filename}"


def avatar_size_validator(value):
    """ Validator for checking avatar size """
    if value.size > 2 * 1024 * 1024:
        raise ValidationError("file size is too big, max: 2Mb")


class Profile(models.Model):
    """ Model for users profile """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True, blank=True, unique=True)
    avatar = models.ImageField(
        null=True, blank=True, upload_to=path_to_img, validators=[avatar_size_validator]
    )
