from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import Entity, Person, Business


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ["id", "name", "meta", "canonical"]


class PersonSerializer(EntitySerializer):
    full_name = serializers.CharField()

    class Meta:
        model = Entity
        fields = ["id", "name", "meta", "canonical", "full_name"]


class BusinessSerializer(EntitySerializer):
    proprietor = PersonSerializer()

    class Meta:
        model = Entity
        fields = ["id", "name", "meta", "proprietor"]


class EntityPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Entity: EntitySerializer,
        Person: PersonSerializer,
        Business: BusinessSerializer,
    }
