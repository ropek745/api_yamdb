import csv
from django.core.management.base import BaseCommand

from review.models import GenreTitle


class Command(BaseCommand):
    help = 'Наполнение БД жанров произведений'

    def handle(self, *args, **options):
        with open('static/data/genre_title.csv', 'r',
                  encoding='UTF-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                GenreTitle.objects.create(
                    title_id=int(row[1]),
                    genre_id=int(row[2])
                )
