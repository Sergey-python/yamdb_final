from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet


class CreateListDestroyViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    """
    ViewSet, поддерживающий ограниченный набор действий.
    Позволяет получить список объектов, создать или удалить объект.
    """

    pass
