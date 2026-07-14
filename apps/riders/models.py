from django.db import models
from apps.common.models import BaseModel


class Rider(BaseModel):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        db_index=True
    )

    nin = models.CharField(
        max_length=11,
        unique=True,
        db_index=True
    )

    address = models.TextField()

    state_of_origin = models.CharField(max_length=100)

    lga = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class NextOfKin(BaseModel):
    rider = models.OneToOneField(
        Rider,
        on_delete=models.CASCADE,
        related_name="next_of_kin"
    )

    name = models.CharField(max_length=200)

    phone_number = models.CharField(max_length=15)

    relationship = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Motorcycle(BaseModel):
    rider = models.OneToOneField(
        Rider,
        on_delete=models.CASCADE,
        related_name="motorcycle"
    )

    plate_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True
    )

    chassis_number = models.CharField(
        max_length=100,
        unique=True
    )

    engine_number = models.CharField(
        max_length=100,
        unique=True
    )

    brand = models.CharField(max_length=100)

    color = models.CharField(max_length=50)

    def __str__(self):
        return self.plate_number