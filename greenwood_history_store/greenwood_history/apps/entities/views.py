from rest_framework import viewsets

from .models import Entity
from .serializers import EntitySerializer


class EntityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Entitys to be viewed or edited.
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer