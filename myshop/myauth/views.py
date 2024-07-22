import json

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .forms import CreateUserForm


class SignInView(APIView):
    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        data = json.loads(request.readline().decode())

        user = authenticate(request=request, username=data.get("username"), password=data.get("password"))
        if user:
            login(request=request, user=user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(CreateAPIView):
    """ Class for registration user """
    @transaction.atomic
    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        data = json.loads(request.readline().decode())
        form = CreateUserForm(data={
            "first_name": data.get("name"),
            "username": data.get("username"),
            "password": data.get("password"),
        })

        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            Profile.objects.get_or_create(user=user)
            login(request=request, user=user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignOutView(APIView, LoginRequiredMixin):
    """ Class for logout user """
    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)


class PaymentView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        pass


class ProfileView(APIView, LoginRequiredMixin):

    def get(self, request: Request, *args, **kwargs) -> Response:
        profile = Profile.objects.get(user=request.user.pk)
        data = {
            "fullName": profile.fullName,
            "email": profile.email,
            "phone": profile.phone,
            "avatar": {
                "src": profile.avatar.url,
                "alt": profile.avatar.name
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data

        result = Profile.objects.update(
            fullname=data["fullName"],
            email=data["email"],
            phone=data["phone"],
            avatar=data["avatar"]
        )
        return Response(status=status.HTTP_200_OK)


class ProfilePasswordView(UpdateAPIView):
    @transaction.atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        user = User.objects.get(username=request.user.username)
        user.password = request.data["newPassword"]
        user.save()
        return Response(status=status.HTTP_200_OK)


class ProfileAvatarView(UpdateAPIView):
    @transaction.atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        form = ProfileAvatarForm(request.FILES)


        user_profile = Profile.objects.get(user=request.user)
        avatar = request.FILES.get("avatar")
        user_profile.avatar = avatar
        user_profile.save()
        return Response(status=status.HTTP_200_OK)
