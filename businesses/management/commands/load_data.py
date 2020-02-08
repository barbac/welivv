import csv
from django.core.management.base import BaseCommand

from businesses.models import Business


def parse_csv(csv_filename):
    with open(csv_filename) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # first line has the headers.
        for row in reader:
            yield Business(
                id=int(row[0]),
                uuid=row[1],
                name=row[2],
                address=row[3],
                address2=row[4],
                city=row[5],
                state=row[6],
                zip=row[7],
                country=row[8],
                phone=row[9],
                website=row[10],
                created_at=row[11],
            )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("load_data", type=str)

    def handle(self, *args, **kwargs):
        businesses = parse_csv(kwargs["load_data"])
        Business.objects.bulk_create(businesses)
