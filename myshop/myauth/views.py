import json

from django.http import HttpRequest
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class SignInView(APIView):
    pass


class SignUpView(CreateAPIView):
    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        a = json.loads(request.readline().decode())
        print(a, type(a))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignOutView(APIView):
    pass
