from datetime import datetime

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .utils import CurrentTitleModelObjDefault


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        exclude = ("review",)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.HiddenField(default=CurrentTitleModelObjDefault())

    class Meta:
        fields = "__all__"
        model = Review
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=("title", "author"),
                message="Вы уже оставляли отзыв на данное произведение!",
            ),
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleSerializerRead(serializers.ModelSerializer):
    """
    Сериализатор модели Title, предоставляющий данные для чтения.
    """

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField()

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title


class TitleSerializerWrite(serializers.ModelSerializer):
    """
    Сериализатор модели Title, берущий данные для записи.
    """

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        fields = "__all__"
        model = Title
        validators = (
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=("name", "year", "category"),
            ),
        )

    def validate_year(self, value):
        now_year = datetime.now().year
        if value > now_year:
            raise ValidationError({"detail": "Проверьте год"})
        return value


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователей."""

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def create(self, validated_data):
        try:
            user, created = User.objects.get_or_create(**validated_data)
        except IntegrityError as error:
            field = str(error).split(".")[1]
            raise ValidationError(
                {"detail": f"Пользователь с таким {field} уже существует!"}
            )
        return user

    def validate_username(self, value):
        if value == "me":
            raise ValidationError(
                {"detail": "Нельзя использовать 'me' в качестве username!"}
            )
        return value


class CustomTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена по коду подтверждения."""

    username = serializers.CharField(
        max_length=User._meta.get_field("username").max_length
    )
    confirmation_code = serializers.CharField(max_length=24)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class MeUserSerializer(UserSerializer):
    """Сериализатор модели User, обрабатывающий эндпоинт /me/."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)
