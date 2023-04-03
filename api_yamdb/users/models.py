from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLE_CHOICES = (
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    )
    email = models.EmailField("email address", max_length=254, unique=True)
    bio = models.TextField("biography", blank=True)
    role = models.CharField(
        "role", max_length=20, choices=ROLE_CHOICES, default=USER
    )

    objects = CustomUserManager()
