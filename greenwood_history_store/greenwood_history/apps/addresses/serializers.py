from rest_framework import serializers

from .models import Address, Street


class StreetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Street
        fields = ["id", "name", "type", "direction"]


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "number", "number_additional", "street"]
