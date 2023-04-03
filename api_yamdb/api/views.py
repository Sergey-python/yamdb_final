from api.filters import TitleFilter
from django.conf import settings
from django.contrib.auth.tokens import (
    default_token_generator as code_generator,
)
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .permissions import (
    IsAdminOrReadOnly,
    IsAdminUser,
    IsStaffOrAuthorOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CustomTokenSerializer,
    GenreSerializer,
    MeUserSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
    UserSerializer,
)
from .viewsets import CreateListDestroyViewSet


class CommentViewSet(ModelViewSet):
    """
    ViewSet, поддерживающий стандартные действия для модели Comment.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_review(self):
        """Метод получения объекта ревью по review_id из url."""
        return get_object_or_404(Review, id=self.kwargs["review_id"])

    def get_queryset(self):
        review = self.get_review()
        return review.comments.select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(ModelViewSet):
    """
    ViewSet, поддерживающий стандартные действия для модели Review.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_title(self):
        """Метод получения объекта произведения по title_id из url."""
        return get_object_or_404(Title, id=self.kwargs["title_id"])

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(CreateListDestroyViewSet):
    """
    ViewSet, поддерживающий ограниченный набор действия для модели Category.
    Позволяет получить список категорий, создать или удалить категорию.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(CreateListDestroyViewSet):
    """
    ViewSet, поддерживающий ограниченный набор действия для модели Genre.
    Позволяет получить список жанров, создать или удалить жанр.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(ModelViewSet):
    """
    ViewSet, поддерживающий стандартные действия для модели Title.
    """

    queryset = (
        Title.objects.prefetch_related("category", "genre")
        .annotate(rating=Avg("reviews__score"))
        .order_by("id")
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleSerializerRead
        return TitleSerializerWrite


class SignUpView(APIView):
    """
    ViewSet, обеспечивающий регистрацию пользователей.
    Зарегестрированные пользователи получают код подтверждения на почту.
    """

    permission_classes = (AllowAny,)

    @classmethod
    def _send_confirmation_code_to_user_email(cls, user, confirmation_code):
        """Метод для отправки кода подтверждения на почту пользователя."""
        subject = settings.EMAIL_SUBJECT
        message = f"{settings.EMAIL_MESSAGE} {confirmation_code}"
        from_email = settings.FROM_EMAIL
        user.email_user(subject, message, from_email)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        confirmation_code = code_generator.make_token(user)
        self._send_confirmation_code_to_user_email(user, confirmation_code)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenView(APIView):
    """
    ViewSet для получения токена по коду подтвержжения.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")
        user = get_object_or_404(User, username=username)
        if not code_generator.check_token(user=user, token=confirmation_code):
            raise ValidationError({"detail": "Неверный код подтвержения!"})
        token = AccessToken.for_user(user)
        return Response({"token": str(token)})


class UserViewSet(ModelViewSet):
    """
    ViewSet, поддерживающий стандартные действия для модели User.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "username"

    def _get_request_user(self):
        """Метод получения пользователя из объекта request."""
        return self.request.user

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=(IsAuthenticated,),
        serializer_class=MeUserSerializer,
    )
    def me(self, request):
        """
        Метод, предоставляющий эндпоинт /me/.
        По нему можно получить/изменить пользовательскую информацию.
        """
        self.get_object = self._get_request_user
        if request.method == "GET":
            return self.retrieve(request)
        return self.partial_update(request)
