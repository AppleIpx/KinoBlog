from drf_spectacular.utils import extend_schema

from some_proj.films.models import FilmModel
from some_proj.films.serializers.film_serializers import AdminFilmSerializer
from some_proj.films.serializers.film_serializers import AdminListFilmSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmGuestSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmSerializer
from some_proj.films.serializers.film_serializers import ListFilmGuestSerializer
from some_proj.films.serializers.film_serializers import ListFilmSerializer
from some_proj.films.serializers.shemas_response import ListFilmResponseSerializers
from some_proj.films.serializers.shemas_response import RetrieveFilmResponseSerializers
from some_proj.films.utils.base_view import BaseContentView


@extend_schema(tags=["Films"])
class FilmsView(BaseContentView):
    serializer_mapping = {
        "staff": {
            "list": AdminListFilmSerializer,
            "detailed": AdminFilmSerializer,
        },
        "authenticated": {
            "list": ListFilmSerializer,
            "detailed": DetailedFilmSerializer,
        },
        "anonymous": {
            "list": ListFilmGuestSerializer,
            "detailed": DetailedFilmGuestSerializer,
        },
    }

    @extend_schema(
        responses={
            200: ListFilmResponseSerializers(),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: RetrieveFilmResponseSerializers(),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.get_annotated_queryset(FilmModel, user, "staff")
        if user.is_authenticated:
            return self.get_annotated_queryset(FilmModel, user, "authenticated")
        return FilmModel.objects.all()
