from rest_framework import serializers

from some_proj.films.serializers.film_serializers import AdminFilmSerializer
from some_proj.films.serializers.film_serializers import AdminListFilmSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmGuestSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmSerializer
from some_proj.films.serializers.film_serializers import ListFilmGuestSerializer
from some_proj.films.serializers.film_serializers import ListFilmSerializer
from some_proj.serials.serializers import AdminListSerialSerializer
from some_proj.serials.serializers import AdminSerialSerializer
from some_proj.serials.serializers import DetailedSerialGuestSerializer
from some_proj.serials.serializers import DetailedSerialSerializer
from some_proj.serials.serializers import ListSerialGuestSerializer
from some_proj.serials.serializers import ListSerialSerializer


class ListFilmResponseSerializers(serializers.Serializer):
    list_auth_film = ListFilmSerializer()
    list_admin_film = AdminListFilmSerializer()
    list_guest_film = ListFilmGuestSerializer()


class RetrieveFilmResponseSerializers(serializers.Serializer):
    retrieve_auth_film = DetailedFilmSerializer()
    retrieve_admin_film = AdminFilmSerializer()
    retrieve_guest_film = DetailedFilmGuestSerializer()


class ListSerialResponseSerializers(serializers.Serializer):
    list_auth_serial = ListSerialSerializer()
    list_admin_serial = AdminListSerialSerializer()
    list_guest_serial = ListSerialGuestSerializer()


class RetrieveSerialResponseSerializers(serializers.Serializer):
    retrieve_auth_serial = DetailedSerialSerializer()
    retrieve_admin_serial = AdminSerialSerializer()
    retrieve_guest_serial = DetailedSerialGuestSerializer()
