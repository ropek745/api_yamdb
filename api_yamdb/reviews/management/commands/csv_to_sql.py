import csv
from django.core.management.base import BaseCommand

from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title,
                            User)


class Command(BaseCommand):
    help = 'Наполнение БД из файлов CSV'

    def handle(self, *args, **options):
        filename = 'static/data/category.csv'
        try:
            with open(
                filename,
                'r',
                encoding='UTF-8'
            ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)
                for row in csv_reader:
                    Category.objects.create(
                        id=row[0],
                        name=row[1],
                        slug=row[2]
                    )
        except FileNotFoundError:
            print(f'Файл {filename} не найден')
        filename = 'static/data/comments.csv'
        try:
            with open(
                filename,
                'r',
                encoding='UTF-8'
            ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)
                for row in csv_reader:
                    review, _ = Review.objects.get_or_create(id=row[1])
                    Comment.objects.create(
                        id=row[0],
                        review=review,
                        text=row[2],
                        author=[3],
                        pub_date=[4]
                    )
        except FileNotFoundError:
            print(f'Файл {filename} не найден')
        filename = 'static/data/genre.csv'
        try:
            with open(
                filename,
                'r',
                encoding='UTF-8'
            ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)
                for row in csv_reader:
                    Genre.objects.create(
                        id=row[0],
                        name=row[1],
                        slug=row[2]
                    )
        except FileNotFoundError:
            print(f'Файл {filename} не найден')
        filename = 'static/data/genre_title.csv'
        try:
            with open(
                filename,
                'r',
                encoding='UTF-8'
            ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)
                for row in csv_reader:
                    title, _ = Title.objects.get_or_create(id=row[1])
                    genre, _ = Genre.objects.get_or_create(id=row[2])
                    GenreTitle.objects.create(
                        id=row[0],
                        title=title,
                        genre=genre
                    )
        except FileNotFoundError:
            print(f'Файл {filename} не найден')
        filename = 'static/data/review.csv'
        try:
            with open(
                filename,
                'r',
                encoding='UTF-8'
            ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)
                for row in csv_reader:
                    title, _ = Title.objects.get_or_create(id=row[1])
                    Review.objects.create(
                        id=row[0],
                        title=title,
                        text=row[2],
                        author=[3],
                        score=[4],
                        pub_date=[5]
                    )
        except FileNotFoundError:
            print(f'Файл {filename} не найден')    
        filename = 'static/data/titles.csv'
        try:
            with open(
                filename,
                'r',
                encoding='UTF-8'
            ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)
                for row in csv_reader:
                    category, _ = Category.objects.get_or_create(id=row[3])
                    Title.objects.create(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category=category
                    )
        except FileNotFoundError:
            print(f'Файл {filename} не найден')    
        filename = 'static/data/users.csv'
        try:
            with open(
                filename,
                'r',
                encoding='UTF-8'
            ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                next(csv_reader)
                for row in csv_reader:
                    User.objects.create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=[3],
                        bio=[4],
                        first_name=[5],
                        last_name=[6]
                    )
        except FileNotFoundError:
            print(f'Файл {filename} не найден')