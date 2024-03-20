from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from some_proj.films.models import FilmModel
from some_proj.films.serializers.film_serializers import AdminFilmSerializer
from some_proj.films.serializers.film_serializers import AdminListFilmSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmGuestSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmSerializer
from some_proj.films.serializers.film_serializers import ListFilmGuestSerializer
from some_proj.films.serializers.film_serializers import ListFilmSerializer


@extend_schema(tags=["Films"])
class FilmsView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    queryset = FilmModel.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        user = self.request.user
        has_pk_param = bool(self.kwargs.get("pk"))
        if has_pk_param:
            self.action = "detailed"
        else:
            self.action = "list"
        role = "staff" if user.is_staff else "authenticated" if user.is_authenticated else "anonymous"

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
        return serializer_mapping[role][self.action]
