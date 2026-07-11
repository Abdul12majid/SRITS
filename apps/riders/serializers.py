from rest_framework import serializers
from .models import Rider, NextOfKin, Motorcycle


class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        exclude = ("rider",)


class MotorcycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycle
        exclude = ("rider",)


class RiderSerializer(serializers.ModelSerializer):
    next_of_kin = NextOfKinSerializer()
    motorcycle = MotorcycleSerializer()

    class Meta:
        model = Rider
        fields = "__all__"

    def create(self, validated_data):
        next_of_kin_data = validated_data.pop("next_of_kin")
        motorcycle_data = validated_data.pop("motorcycle")

        rider = Rider.objects.create(**validated_data)

        NextOfKin.objects.create(
            rider=rider,
            **next_of_kin_data
        )

        Motorcycle.objects.create(
            rider=rider,
            **motorcycle_data
        )

        return rider