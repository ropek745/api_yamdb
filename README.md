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
## Документация API ##
У проекта есть документация к API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов.

Для её просмотра нужно перейти на эндпоинт `http://127.0.0.1:8000/redoc/`.

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
  - [Роман Пекарев](https://github.com/ropek745)
  - [Никита Цыбин](https://github.com/kellia1903)
  - [Оксана Широкова](https://github.com/son13425)
