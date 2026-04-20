from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from time_ranges.models import TimeRange, EntityAddressTimeRangeThrough


class RangeRelationsTest(TestCase):
    def setUp(self):
        self.person = baker.make("entities.Person")
        self.address = baker.make("addresses.Address")
        # self.range = baker.make(TimeRange)
        self.range_1919 = TimeRange.objects.get(name="1919")
        self.range_1920 = TimeRange.objects.get(name="1920")

    def test_queryset_date_in(self):
        date = timezone.datetime(2020, 2, 1)
        ranges = TimeRange.objects.date_in(date)
        self.assertSequenceEqual(ranges, [])

    def test_queryset_date_in_contains_ranges(self):
        date = timezone.datetime(1920, 2, 1)
        ranges = TimeRange.objects.date_in(date)
        self.assertSequenceEqual(ranges, [self.range_1920])

    # def test_holds_person_entity(self):
    #     eatr1 = baker.make(
    #         EntityAddressTimeRange,
    #         entity=self.person,
    #         address=self.address,
    #         time_range=self.range_1919,
    #     )
    #     eatr2 = baker.make(
    #         EntityAddressTimeRange,
    #         entity=self.person,
    #         address=self.address,
    #         time_range=self.range_1920,
    #     )

    # TimeRange.objects.

    def test_add_entity_through(self):
        # self.range_1919.entities.add(self.person)
        self.range_1919.entities.add(self.person, through_defaults=dict(address=self.address))
        range_entities = self.range_1919.entities.all()
        self.assertEqual(range_entities.count(), 1)
        # self.range_1919.entities.add(self.person, self.address)
