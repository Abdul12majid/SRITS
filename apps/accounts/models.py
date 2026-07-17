from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import timedelta
from django.utils import timezone
import random
from apps.common.models import BaseModel

class OTP(BaseModel):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    @staticmethod
    def generate():
        return str(random.randint(100000, 999999))


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required.")

        user = self.model(
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            phone_number,
            password,
            **extra_fields
        )


class User(AbstractUser):

    class Roles(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        PMS_ADMIN = "PMS_ADMIN", "PMS Admin"
        REGISTRATION_OFFICER = (
            "REGISTRATION_OFFICER",
            "Registration Officer",
        )
        ENFORCEMENT_OFFICER = (
            "ENFORCEMENT_OFFICER",
            "Enforcement Officer",
        )
        RIDER = "RIDER", "Rider"

    username = None

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
    )

    role = models.CharField(
        max_length=30,
        choices=Roles.choices,
        default=Roles.RIDER,
    )

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"