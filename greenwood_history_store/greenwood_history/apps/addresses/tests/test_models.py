from django.test import TestCase
from addresses.models import Directions, Street, StreetTypes, parse_street_name
import pytest


def test_parse_street_name():
    assert parse_street_name("aardvark") == ("Aardvark", None, StreetTypes.ST.value)
    assert parse_street_name("aardvark-N") == (
        "Aardvark",
        Directions.NORTH.value,
        StreetTypes.ST.value,
    )
    assert parse_street_name("aardvark-N Ave.") == (
        "Aardvark",
        Directions.NORTH.value,
        StreetTypes.AVE.value,
    )
    assert parse_street_name("Aardvark St.") == ("Aardvark", None, StreetTypes.ST.value)
    assert parse_street_name("aardvark-S Blvd.") == (
        "Aardvark",
        Directions.SOUTH.value,
        StreetTypes.BLVD.value,
    )
    assert parse_street_name("aardvark-S Blvd") == (
        "Aardvark",
        Directions.SOUTH.value,
        StreetTypes.BLVD.value,
    )
    # test cases for direction after street type
    assert parse_street_name("Cruce Ave.-N") == (
        "Cruce",
        Directions.NORTH.value,
        StreetTypes.AVE.value,
    )
    assert parse_street_name("Cruce Ave.-S") == (
        "Cruce",
        Directions.SOUTH.value,
        StreetTypes.AVE.value,
    )
    assert parse_street_name("Cruce Ave.-") == (
        "Cruce",
        None,
        StreetTypes.AVE.value,
    )


class StreetTest(TestCase):
    def test_get_or_create_from_name(self):
        "TODO: mock out parse_street_name and test different return value conditions"
        pass
