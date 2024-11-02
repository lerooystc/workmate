from apps.showcase.models import Breed
from apps.showcase.models import Dog
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from drf_spectacular.utils import OpenApiResponse
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import BreedSerializer
from .serializers import DogSerializer
from .serializers import ReadBreedSerializer
from .serializers import ReadDogSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Порода"],
        responses={
            200: OpenApiResponse(
                response=ReadBreedSerializer, description="Список пород."
            ),
            400: OpenApiResponse(
                description="Инвалидные данные. Не удалось получить породы."
            ),
        },
    ),
    retrieve=extend_schema(
        tags=["Порода"],
        responses={
            200: OpenApiResponse(
                response=ReadBreedSerializer, description="Получены данные о породе."
            ),
            404: OpenApiResponse(description="Порода не найдена."),
        },
    ),
    create=extend_schema(
        tags=["Порода"],
        responses={
            201: OpenApiResponse(
                response=BreedSerializer, description="Создана порода."
            ),
            400: OpenApiResponse(
                description="Не удалось создать породу. Инвалидные данные."
            ),
        },
    ),
    update=extend_schema(
        tags=["Порода"],
        responses={
            200: OpenApiResponse(
                response=BreedSerializer, description="Изменены данные о породе."
            ),
            400: OpenApiResponse(
                description="Не удалось создать породу. Инвалидные данные."
            ),
            404: OpenApiResponse(description="Порода не найдена."),
        },
    ),
    destroy=extend_schema(
        tags=["Порода"],
        responses={
            204: OpenApiResponse(description="Удалены данные о породы."),
            404: OpenApiResponse(description="Порода не найдена."),
        },
    ),
)
class BreedViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Breed.objects.order_by("id")
    serializer_class = BreedSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["get", "post", "put", "delete"]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadBreedSerializer
        return super().get_serializer_class()


@extend_schema_view(
    list=extend_schema(
        tags=["Собака"],
        responses={
            200: OpenApiResponse(response=DogSerializer, description="Список собак."),
            400: OpenApiResponse(
                description="Инвалидные данные (порода). Не удалось получить собак."
            ),
        },
    ),
    retrieve=extend_schema(
        tags=["Собака"],
        responses={
            200: OpenApiResponse(
                response=ReadDogSerializer, description="Получены данные о собак."
            ),
            404: OpenApiResponse(description="Собака не найдена."),
        },
    ),
    create=extend_schema(
        tags=["Собака"],
        responses={
            201: OpenApiResponse(response=DogSerializer, description="Создана собака."),
            400: OpenApiResponse(
                description="Не удалось создать собаку. Инвалидные данные."
            ),
        },
    ),
    update=extend_schema(
        tags=["Собака"],
        responses={
            200: OpenApiResponse(
                response=DogSerializer, description="Изменены данные о собаке."
            ),
            400: OpenApiResponse(
                description="Не удалось создать собаку. Инвалидные данные."
            ),
            404: OpenApiResponse(description="Собака не найдена."),
        },
    ),
    destroy=extend_schema(
        tags=["Собака"],
        responses={
            204: OpenApiResponse(description="Удалены данные о собаке."),
            403: OpenApiResponse(description="Нет прав доступа на удаление собаки."),
            404: OpenApiResponse(description="Собака не найдена."),
        },
    ),
)
class DogViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Dog.objects.select_related("breed").order_by("-id")
    serializer_class = DogSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["get", "post", "put", "delete"]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadDogSerializer
        return super().get_serializer_class()

    def create(self, request):
        serializer = DogSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            instance = serializer.save()
            response_object = ReadDogSerializer(instance)
            return Response(response_object.data, status=status.HTTP_201_CREATED)
        return Response(
            {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
        )
