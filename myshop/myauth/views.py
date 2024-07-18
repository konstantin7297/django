import json

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CreateUserForm
from .models import Profile


class SignInView(APIView):
    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        data = json.loads(request.readline().decode())
        user = User.objects.get(username=data['username'], password=data['password'])

        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(CreateAPIView):
    @transaction.atomic
    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        data = json.loads(request.readline().decode())
        data["first_name"] = data["name"]

        form = CreateUserForm(data=data)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignOutView(APIView, LoginRequiredMixin):
    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)
