from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "phone_number", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        User = get_user_model()
        try:
            user = User.objects.get(phone_number=data["phone_number"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this phone number does not exist"
            )

        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Invalid credentials")

        return user
