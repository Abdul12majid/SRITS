from django.contrib import admin
from .models import RiderDocument


@admin.register(RiderDocument)
class RiderDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "rider",
        "document_type",
        "uploaded_by",
        "created_at",
    )

    list_filter = (
        "document_type",
        "created_at",
    )

    search_fields = (
        "rider__first_name",
        "rider__last_name",
        "rider__phone_number",
    )