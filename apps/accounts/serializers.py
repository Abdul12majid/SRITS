from rest_framework import serializers
from .models import User

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(
        write_only=True
    )

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        )

class RequestOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(
        write_only=True,
        min_length=6,
    )