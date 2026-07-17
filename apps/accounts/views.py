from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, LogoutSerializer, UserSerializer
from .serializers import RequestOTPSerializer, VerifyOTPSerializer, ResetPasswordSerializer
from datetime import timedelta
from django.utils import timezone
from .models import User, OTP


@api_view(["GET"])
def me(request):
    serializer = UserSerializer(request.user)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    phone_number = serializer.validated_data["phone_number"]
    password = serializer.validated_data["password"]

    user = authenticate(
        request,
        phone_number=phone_number,
        password=password,
    )

    if user is None:
        return Response(
            {"error": "Invalid phone number or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "role": user.role,
            },
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    serializer = LogoutSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = RefreshToken(serializer.validated_data["refresh"])
        token.blacklist()

        return Response({
            "message": "Logged out successfully."
        })

    except Exception:
        return Response(
            {
                "error": "Invalid refresh token."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["POST"])
@permission_classes([AllowAny])
def request_otp(request):
    serializer = RequestOTPSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    phone_number = serializer.validated_data["phone_number"]

    if not User.objects.filter(phone_number=phone_number).exists():
        return Response(
            {
                "error": "User not found."
            },
            status=404,
        )

    OTP.objects.filter(
        phone_number=phone_number,
        is_used=False,
    ).delete()

    code = OTP.generate()

    OTP.objects.create(
        phone_number=phone_number,
        otp=code,
        expires_at=timezone.now() + timedelta(minutes=5),
    )

    return Response(
        {
            "message": "OTP generated successfully.",
            "otp": code #will change to provider later
        }
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data

    try:
        otp = OTP.objects.get(
            phone_number=data["phone_number"],
            otp=data["otp"],
            is_used=False,
        )
    except OTP.DoesNotExist:
        return Response(
            {
                "error": "Invalid OTP."
            },
            status=400,
        )

    if otp.is_expired():
        return Response(
            {
                "error": "OTP has expired."
            },
            status=400,
        )

    otp.is_used = True
    otp.save()

    return Response(
        {
            "message": "OTP verified."
        }
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data

    try:
        otp = OTP.objects.get(
            phone_number=data["phone_number"],
            otp=data["otp"],
            is_used=True,
        )
    except OTP.DoesNotExist:
        return Response(
            {
                "error": "OTP verification required."
            },
            status=400,
        )

    user = User.objects.get(
        phone_number=data["phone_number"]
    )

    user.set_password(data["password"])

    user.save()

    otp.delete()

    return Response(
        {
            "message": "Password updated successfully."
        }
    )