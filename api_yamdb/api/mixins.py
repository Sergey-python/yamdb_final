from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response


class CreateModelHTTP200Mixin(CreateModelMixin):
    """
    Mixin, изменяющий статус ответа при создания объекта.
    Статус HTTP_201_CREATED заменен на HTTP_200_OK.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )
