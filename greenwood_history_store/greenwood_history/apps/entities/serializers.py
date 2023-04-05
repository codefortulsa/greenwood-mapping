from rest_framework import serializers

from .models import Entity


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entity
        fields = ["name", "meta"]
