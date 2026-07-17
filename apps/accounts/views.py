from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, LogoutSerializer


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