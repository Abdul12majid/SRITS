from django.contrib import admin
from .models import Rider, NextOfKin, Motorcycle


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone_number",
        "nin",
        "state_of_origin",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone_number",
        "nin",
    )

    list_filter = (
        "gender",
        "state_of_origin",
    )


@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "relationship",
        "rider",
    )

    search_fields = (
        "name",
        "phone_number",
    )


@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    list_display = (
        "plate_number",
        "brand",
        "color",
        "rider",
    )

    search_fields = (
        "plate_number",
        "engine_number",
        "chassis_number",
    )