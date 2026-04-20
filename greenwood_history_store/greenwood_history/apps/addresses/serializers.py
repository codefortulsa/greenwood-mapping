from rest_framework import serializers

from .models import Address, Street


class StreetSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()

    class Meta:
        model = Street
        fields = ["id", "name", "type", "direction", "full_name", "short_name"]

    def get_full_name(self, obj):
        return str(obj)

    def get_short_name(self, obj):
        return obj.short_name


class AddressSerializer(serializers.ModelSerializer):
    street = StreetSerializer()

    class Meta:
        model = Address
        fields = ["id", "number", "number_additional", "street"]
