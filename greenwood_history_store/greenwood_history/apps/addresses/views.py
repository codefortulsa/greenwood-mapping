from rest_framework import viewsets

from .models import Address, Street
from .serializers import AddressSerializer, StreetSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Addresses to be viewed or edited.
    """

    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class StreetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Streetses to be viewed or edited.
    """

    queryset = Street.objects.all()
    serializer_class = StreetSerializer
