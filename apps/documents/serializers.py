from rest_framework import serializers

from .models import RiderDocument


class RiderDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderDocument
        fields = (
            "id",
            "rider",
            "document_type",
            "file",
            "uploaded_by",
            "created_at",
        )
        read_only_fields = (
            "id",
            "uploaded_by",
            "created_at",
        )