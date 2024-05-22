from drf_spectacular.utils import extend_schema
from rest_framework.serializers import Serializer

from some_proj.films.serializers.shemas_response import ListSerialResponseSerializers
from some_proj.films.serializers.shemas_response import RetrieveSerialResponseSerializers
from some_proj.films.utils.base_view import BaseContentView
from some_proj.serials.models import SerialModel
from some_proj.serials.serializers import AdminListSerialSerializer
from some_proj.serials.serializers import AdminSerialSerializer
from some_proj.serials.serializers import DetailedSerialGuestSerializer
from some_proj.serials.serializers import DetailedSerialSerializer
from some_proj.serials.serializers import ListSerialGuestSerializer
from some_proj.serials.serializers import ListSerialSerializer


@extend_schema(tags=["Serials"])
class SerialsView(BaseContentView):
    serializer_mapping: dict[str, dict[str, type[Serializer]]] = {
        "staff": {
            "list": AdminListSerialSerializer,
            "detailed": AdminSerialSerializer,
        },
        "authenticated": {
            "list": ListSerialSerializer,
            "detailed": DetailedSerialSerializer,
        },
        "anonymous": {
            "list": ListSerialGuestSerializer,
            "detailed": DetailedSerialGuestSerializer,
        },
    }

    @extend_schema(
        description="Отображение списка фильмов",
        responses={
            200: ListSerialResponseSerializers(),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Отображение конкретного фильма",
        responses={
            200: RetrieveSerialResponseSerializers(),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.get_annotated_queryset(SerialModel, user, "staff")
        if user.is_authenticated:
            return self.get_annotated_queryset(SerialModel, user, "authenticated")
        return SerialModel.objects.all()
