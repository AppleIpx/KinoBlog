from rest_framework import permissions
from rest_framework import viewsets

from some_proj.films.models import FilmModel
from some_proj.films.serializers import AdminFilmSerializer
from some_proj.films.serializers import AdminListFilmSerializer
from some_proj.films.serializers import DetailedFilmGuestSerializer
from some_proj.films.serializers import DetailedFilmSerializer
from some_proj.films.serializers import ListFilmGuestSerializer
from some_proj.films.serializers import ListFilmSerializer


class FilmsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = FilmModel.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        has_pk_param = bool(self.kwargs.get("pk"))

        serializer_mapping = {
            "authenticated": DetailedFilmSerializer if has_pk_param else ListFilmSerializer,
            "anonymous": DetailedFilmGuestSerializer if has_pk_param else ListFilmGuestSerializer,
            "staff": AdminFilmSerializer if has_pk_param else AdminListFilmSerializer,
        }
        role = "staff" if user.is_staff else "authenticated" if user.is_authenticated else "anonymous"
        return serializer_mapping.get(role)
