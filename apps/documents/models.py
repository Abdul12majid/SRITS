from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.riders.models import Rider


class RiderDocument(BaseModel):
    DOCUMENT_TYPES = (
        ("NIN", "NIN Slip"),
        ("LICENSE", "Driver's License"),
        ("VEHICLE", "Vehicle Papers"),
        ("ADDRESS", "Proof of Address"),
        ("OTHER", "Other"),
    )

    rider = models.ForeignKey(
        Rider,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES,
    )

    file = models.FileField(
        upload_to="rider_documents/"
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_documents",
    )

    def __str__(self):
        return f"{self.rider} - {self.document_type}"