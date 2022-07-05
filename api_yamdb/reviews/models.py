from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_year

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Админ'),
)


class User(AbstractUser):

    bio = models.TextField(
        blank=True,
        null=False,
        verbose_name='Биография'
    )
    first_name = models.TextField(
        max_length=150,
        blank=True,
        null=False,
        verbose_name='Имя'
    )
    last_name = models.TextField(
        max_length=150,
        blank=True,
        null=False,
        verbose_name='Фамилия'
    )
    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )
    email = models.EmailField(verbose_name='Почта', unique=True)
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True,
        unique=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True
    )

    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ["username", ]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Дата выхода'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'


class ReviewCommentBase(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Review(ReviewCommentBase):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )

    class Meta:
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='review_once'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(ReviewCommentBase):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Название категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Название жанра'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name
