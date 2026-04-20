from rest_framework import viewsets

from .models import Address, Street
from .serializers import AddressSerializer, StreetSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Addresses to be viewed or edited.
    """

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_fields = [
        "number",
        "number_additional",
        "street",
        "street__name",
        "street__type",
        "street__direction",
    ]
    search_fields = ("number", "street__name")


class StreetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Streets to be viewed or edited.
    """

    queryset = Street.objects.all()
    serializer_class = StreetSerializer
