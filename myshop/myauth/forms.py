from django import forms

from .models import Profile


from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user", "fullName", "email", "phone", "avatar"]


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "username", "password"]
