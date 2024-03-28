from drf_spectacular.utils import extend_schema

from some_proj.films.views import BaseContentView
from some_proj.serials.models import SerialModel
from some_proj.serials.serializers import AdminListSerialSerializer
from some_proj.serials.serializers import AdminSerialSerializer
from some_proj.serials.serializers import DetailedSerialGuestSerializer
from some_proj.serials.serializers import DetailedSerialSerializer
from some_proj.serials.serializers import ListSerialGuestSerializer
from some_proj.serials.serializers import ListSerialSerializer


@extend_schema(tags=["Serials"])
class SerialsView(BaseContentView):
    serializer_mapping = {
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

    def get_queryset(self):
        return SerialModel.objects.all().prefetch_related(
            "country",
            "producers",
            "genre",
            "actors",
            "reaction",
        )
