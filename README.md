Проект YaMDb
========================================================
Проект YaMDb собирает отзывы пользователей на произведения
## Технологии
- Python 3.7
- Djagon
- Django REST Framework
- SQLite3
## Как развернуть и запустить проект у себя? ##
### 1. Склонировать репозиторий в рабочее пространство: ###
```
git clone git@github.com:ropek745/api_yamdb.git
```
### 2. Создать и активировать виртуальное окружение. ###
```
python -m venv venv
. venv/Scripts/activate
```
### 3. Установить зависимости из файла requirements.txt. ###
```
pip install -r requirements.txt
```
### 4. Выполнить миграции. ###
```
python manage.py migrate
```
### 5. Запустить проект. ###
```
python manage.py runserver
```
## Эндпоинты проекта ##
- http://127.0.0.1:8000/api/v1/auth/signup/ - получение кода подверждения на email. Доступны только `POST` запросы.

- http://127.0.0.1:8000/api/v1/auth/token/ - получение токена для авторизации. Доступны только `POST` запросы.

- http://127.0.0.1:8000/api/v1/categories/ - категории. Доступны `GET`, `POST` и `DEL` запросы.

- http://127.0.0.1:8000/api/v1/genres/ - жанры. Доступны `GET`, `POST` и `DEL` запросы.

- http://127.0.0.1:8000/api/v1/titles/ - произведения. Доступны `GET`, `POST`, `PATCH` и `DEL` запросы.

- http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/ - отзывы о произведениях. Доступны `GET`, `POST`, `PATCH` и `DEL` запросы.

- http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/ - комментарии для отзывов. Доступны `GET`, `POST`, `PATCH` и `DEL` запросы.

- http://127.0.0.1:8000/api/v1/users/ - получение информации о всех пользователях. Доступны запросы `GET` и `POST`.

- http://127.0.0.1:8000/api/v1/users/{username}/ - получение информации о конкретном пользователе и редактирование информации о нем. Доступны `GET`, `POST` и `DEL` запросы.

- http://127.0.0.1:8000/api/v1/users/me/ - получение и изменение своих данных. Доступны запросы `GET`, `PATCH`.

## Загрузка базы данных из файлов CSV ##
### 1 Система обрабатывает файлы со следующими именами: ###
  - categoty.csv;
  - comments.csv;
  - genre_title.csv;
  - genre.csv;
  - review.csv;
  - titles.csv;
  - users.csv.
### 2 Загрузить файлы CSV по адресу: ###
  api_yamdb/static/data
### 3 Выполнить команду: ###
  ```
  python manage.py csv_to_sql
  ```

## Разработчики ##
  - Роман Пекарев - (https://github.com/ropek745)
  - Никита Цыбин - (https://github.com/kellia1903)
  - Оксана Широкова - (https://github.com/son13425)
