import csv
from django.core.management.base import BaseCommand

from review.models import Genre


class Command(BaseCommand):
    help = 'Наполнение БД жанров'

    def handle(self, *args, **options):
        with open('static/data/genre.csv', 'r', encoding='UTF-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                Genre.objects.create(name=row[1], slug=row[2])
