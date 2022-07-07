from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Category, Comment, Genre, Review, Title, User,
    USERNAME_LENGTH, EMAIL_LENGTH, CONFIRMATION_CODE_LENGTH
)
from .validators import UserValidator


class SignUpSerializer(serializers.Serializer, UserValidator):
    username = serializers.CharField(max_length=USERNAME_LENGTH)
    email = serializers.EmailField(max_length=EMAIL_LENGTH)


class GetTokenSerializer(serializers.Serializer, UserValidator):
    username = serializers.CharField(max_length=USERNAME_LENGTH)
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH
    )


class UserSerializer(serializers.ModelSerializer, UserValidator):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'role', 'bio'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context[
                    'kwargs'].get('title_id')
            )
            title = get_object_or_404(Title, pk=title_id)
            user = self.context['request'].user
            if Review.objects.filter(author=user, title=title).exists():
                raise ValidationError(
                    'Возможен только один отзыв на произведение!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category', 'id')

    def validate_year(self, value):
        year_today = timezone.now().year
        if value > year_today:
            raise ValidationError(
                f'Неверный год {value}. Проверьте год создания!'
            )
        return value


class GetTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        read_only_fields = ('__all__',)
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )
