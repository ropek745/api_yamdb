import csv
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Comment, Genre,
    GenreTitle, Review, Title, User
)


class Command(BaseCommand):
    help = 'Наполнение БД из файлов CSV'

    def handle(self, *args, **options):
        with open(
                'static/data/users.csv',
                'r',
                encoding='UTF-8'
        ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )
        with open(
                'static/data/category.csv',
                'r',
                encoding='UTF-8'
        ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )
        with open(
                'static/data/genre.csv',
                'r',
                encoding='UTF-8'
        ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                Genre.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )
        with open(
                'static/data/titles.csv',
                'r',
                encoding='UTF-8'
        ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                category = Category.objects.get(id=row[3])
                Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=category
                )
        with open(
                'static/data/genre_title.csv',
                'r',
                encoding='UTF-8'
        ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                title = Title.objects.get(id=row[1])
                genre = Genre.objects.get(id=row[2])
                GenreTitle.objects.get_or_create(
                    id=row[0],
                    title=title,
                    genre=genre
                )
        with open(
                'static/data/review.csv',
                'r',
                encoding='UTF-8'
        ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                title = Title.objects.get(id=row[1])
                author = User.objects.get(id=row[3])
                Review.objects.get_or_create(
                    id=row[0],
                    title=title,
                    text=row[2],
                    author=author,
                    score=row[4]
                )
                Review.objects.filter(pk=row[0]).update(pub_date=row[5])
        with open(
                'static/data/comments.csv',
                'r',
                encoding='UTF-8'
        ) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                review = Review.objects.get(id=row[1])
                author = User.objects.get(id=row[3])
                Comment.objects.get_or_create(
                    id=row[0],
                    review=review,
                    text=row[2],
                    author=author
                )
                Comment.objects.filter(pk=row[0]).update(pub_date=row[4])

