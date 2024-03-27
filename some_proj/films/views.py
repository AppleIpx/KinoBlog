from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import viewsets

from some_proj.films.models import FilmModel
from some_proj.films.serializers.film_serializers import AdminFilmSerializer
from some_proj.films.serializers.film_serializers import AdminListFilmSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmGuestSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmSerializer
from some_proj.films.serializers.film_serializers import ListFilmGuestSerializer
from some_proj.films.serializers.film_serializers import ListFilmSerializer


class BaseContentView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_mapping = {
        "list": None,
        "detailed": None,
    }

    def get_serializer_class(self):
        user = self.request.user
        has_pk_param = bool(self.kwargs.get("pk"))
        if has_pk_param:
            self.action = "detailed"
        else:
            self.action = "list"
        role = "staff" if user.is_staff else "authenticated" if user.is_authenticated else "anonymous"
        return self.serializer_mapping[role][self.action]


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
        description="Отображение списка фильмов",
        responses={
            200: ListFilmGuestSerializer(),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Отображение конкретного фильма",
        responses={200: AdminFilmSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return FilmModel.objects.all().prefetch_related(
            "country",
            "producers",
            "genre",
            "actors",
            "reaction",
        )
