import json

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
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
from .forms import ProfileForm, CreateUserForm
from .serializers import ProfileSerializer


class SignInView(APIView):
    """ Class for login user """
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs) -> Response:
        data = json.loads(request.readline().decode())

        user = authenticate(
            request=request,
            username=data.get("username"),
            password=data.get("password")
        )

        if user:
            login(request=request, user=user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(CreateAPIView):
    """ Class for registration user """
    @staticmethod
    @transaction.atomic
    def post(request: HttpRequest, *args, **kwargs) -> Response:
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
    @staticmethod
    def post(request: HttpRequest, *args, **kwargs) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileView(APIView, LoginRequiredMixin):
    """ Class for getting and update user profile information """
    @staticmethod
    def get(request: Request, *args, **kwargs) -> Response:
        return Response(
            data=ProfileSerializer(
                Profile.objects.get(user=User.objects.get(pk=request.user.pk))
            ).data,
            status=status.HTTP_200_OK
        )

    @staticmethod
    @transaction.atomic
    def post(request: Request, *args, **kwargs) -> Response:
        user = User.objects.get(pk=request.user.pk)
        data = request.data
        data["user"] = user

        form = ProfileForm(data=data, instance=user.profile)
        if form.is_valid():
            form.save()

            return Response(
                data=ProfileSerializer(Profile.objects.get(user=user)).data,
                status=status.HTTP_200_OK
            )

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfilePasswordView(UpdateAPIView, LoginRequiredMixin):
    """ Class for changing user password """
    @staticmethod
    @transaction.atomic
    def post(request: Request, *args, **kwargs) -> Response:
        user = authenticate(
            request=request,
            username=request.user.username,
            password=request.data.get("currentPassword")
        )

        if user:
            user.password = make_password(request.data.get("newPassword"))
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileAvatarView(UpdateAPIView, LoginRequiredMixin):
    """ Class for updating user avatar """
    @staticmethod
    @transaction.atomic
    def post(request: Request, *args, **kwargs) -> Response:
        user = User.objects.get(pk=request.user.pk)
        data = {
            "user": user,
            "fullName": user.profile.fullName,
            "email": user.profile.email,
            "phone": user.profile.phone,
        }

        form = ProfileForm(data=data, files=request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
