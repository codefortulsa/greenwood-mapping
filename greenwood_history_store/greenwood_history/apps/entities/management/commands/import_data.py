"""
STREET
NO
1920 city directory
1921 city directory
1922 city directory
1923 city dir.
1920 census/head of residence
listof losses (Parrish book)
Notes
"""
import logging
from csv import DictReader

from buildings.models import Building
from addresses.models import Street, Address
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# from ...models import Business, Entity, Person

logger = logging.getLogger(__name__)


null_values = [
    "address not listed",
    "not listed",
    "street not listed",  # could mean streat is gone or destroyed or didn't exist yet.
]


class Command(BaseCommand):
    help = "Import data from entities csv files."

    def handle(self, **options):
        with open(settings.BASE_DIR / "../data/residents.csv") as file:
            reader = DictReader(file)
            for row in reader:
                try:
                    # Find or create street
                    street_name = row["street"]
                    if street_name == "":
                        continue

                    street, street_created = Street.get_or_create_from_name(street_name)

                    building_number = row["no"]
                    if building_number == "" or street is None:
                        logger.info("no building number, skipped: %s", row)
                        continue

                    address, address_created = Address.get_or_create_from_unique(
                        street=street, number=building_number
                    )

                    print(address, address_created)

                except Exception as e:
                    logger.error("Error importing row: %s", row, exc_info=e)
                    continue
