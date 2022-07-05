from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User
from .validators import validate_username


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=150, required=True,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Неккоректный юзернейм "me"')
        return value


class GetTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Неверный код подтверждения')
        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Неккоректный юзернейм "me"')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = '__all__'
        model = Review

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
            raise ValidationError('Проверьте год создания!')
        return value


class GetTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('name', 'year', 'description', 'genre', 'category',
                            'rating', 'id')
