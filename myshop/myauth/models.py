from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime


def path_to_avatar(instance: "Profile", filename: str) -> str:
    return f"profiles/profile_{instance.pk}/avatar/{filename}"


def avatar_size_validator(value):
    if value.size > 2 * 1024 * 1024:
        raise ValidationError("file size is too big, max: 2Mb")


def payment_month_validator(value):
    if str(value) not in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        raise ValidationError("Invalid payment month")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True, blank=True, unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=path_to_avatar, validators=[
        avatar_size_validator
    ])


class Payment(models.Model):
    number = models.PositiveBigIntegerField(unique=True, validators=[
        MinValueValidator(10000000), MaxValueValidator(99999999)
    ])
    name = models.CharField(max_length=50)
    month = models.PositiveSmallIntegerField(validators=[payment_month_validator])
    year = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(datetime.now().year), MaxValueValidator(datetime.now().year + 3)
    ])
    code = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(100), MaxValueValidator(999)
    ])
