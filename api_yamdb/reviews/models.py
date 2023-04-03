from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime

User = get_user_model()


class Category(models.Model):
    """Модель категорий произведений."""

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""

    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=255)
    year = models.IntegerField(db_index=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(Genre)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "year", "category"], name="unique_title"
            )
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов по произведению."""

    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.SmallIntegerField(
        validators=(
            MinValueValidator(settings.REVIEW_MIN_SCORE),
            MaxValueValidator(settings.REVIEW_MAX_SCORE),
        ),
        error_messages={
            "validators": f"Поставьте оценку от {settings.REVIEW_MIN_SCORE}"
            f" до {settings.REVIEW_MAX_SCORE}"
        },
        default=settings.REVIEW_MIN_SCORE,
    )

    @property
    def csv_pub_date(self):
        return self.pub_date

    @csv_pub_date.setter
    def csv_pub_date(self, value):
        if value:
            self.pub_date = datetime.datetime.strptime(
                value, settings.CSV_DATETIME_FORMAT
            )

    class Meta:
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев по отзыву."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    @property
    def csv_pub_date(self):
        return self.pub_date

    @csv_pub_date.setter
    def csv_pub_date(self, value):
        if value:
            self.pub_date = datetime.datetime.strptime(
                value, settings.CSV_DATETIME_FORMAT
            )

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text
