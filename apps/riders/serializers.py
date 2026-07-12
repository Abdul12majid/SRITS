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

    def update(self, instance, validated_data):
        next_of_kin_data = validated_data.pop("next_of_kin", None)
        motorcycle_data = validated_data.pop("motorcycle", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if next_of_kin_data:
            next_of_kin = instance.next_of_kin

            for attr, value in next_of_kin_data.items():
                setattr(next_of_kin, attr, value)

            next_of_kin.save()

        if motorcycle_data:
            motorcycle = instance.motorcycle

            for attr, value in motorcycle_data.items():
                setattr(motorcycle, attr, value)

            motorcycle.save()

        return instance

    def validate_nin(self, value):
        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError("NIN must contain only numbers.")

        if len(value) != 11:
            raise serializers.ValidationError("NIN must be exactly 11 digits.")

        return value


    def validate_phone_number(self, value):
        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only numbers.")

        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")

        return value


    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be in the future."
            )

        return value