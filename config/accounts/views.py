# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import random
from .models import User
from django.core.cache import cache
import requests
from decouple import config


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_otp(request):
    if request.method == "POST":
        randomed_code = str(random.randint(1000, 9999))
        user = User.objects.get(pk=request.user.id)

        phone_number = user.phone_number
        phone_number = str(phone_number)

        cache_key = f"otp_{phone_number}"

        cache.set(cache_key, randomed_code, 120)

        url = "https://api.sms.ir/v1/send/verify"

        header = {
            "Content-Type": "application/json",
            "Accept": "text/plain",
            "x-api-key": config("API_KEY"),
        }

        request_data = {
            "mobile": phone_number.split("+98")[1],
            "templateId": 123456,
            "parameters": [{"name": {"Code"}, "value": {randomed_code}}],
        }

        response = requests.post(url, headers=header, json=request_data)

        if response.status_code == 200:
            return Response(
                {"message": "OTP sent successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Something went wrong"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def verify_otp(request):
    if request.method == "POST":
        code = request.data.get("code")
        phone_number = User.objects.get(pk=request.user.id).phone_number

        cache_key = f"otp_{phone_number}"
        cached_otp = cache.get(cache_key)

        if code == cached_otp:
            cache.delete(cache_key)
            user = request.user
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "OTP verified successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "OTP verification failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
