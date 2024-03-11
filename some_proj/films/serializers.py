from rest_framework import serializers

from some_proj.comments.serializers import CommentSerializer
from some_proj.contrib.mixins import FavoriteMixin
from some_proj.contrib.mixins import SeeLateMixin
from some_proj.contrib.mixins import WatchMixin
from some_proj.films.models import ActorModel
from some_proj.films.models import FilmContentModel
from some_proj.films.models import PhotoFilm
from some_proj.media_for_kino_card.serializers import MediaSerializer


class BaseSerializer(FavoriteMixin, serializers.ModelSerializer):
    poster = serializers.ImageField()


class FilmSerializer(BaseSerializer):
    class Meta:
        model = FilmContentModel
        fields = [
            "id",
            "name",
            "release_date",
            "age_limit",
            "poster",
            "is_favorite",
        ]


class FilmGuestSerializer(FilmSerializer):
    is_favorite = None

    class Meta(FilmSerializer.Meta):
        fields = [
            *FilmSerializer.Meta.fields,
        ].remove("is_favorite")


class ListFilmSerializer(FilmSerializer):
    class Meta(FilmSerializer.Meta):
        fields = [
            *FilmSerializer.Meta.fields,
            "duration",
            "reaction_like",
            "reaction_dislike",
        ]


class ListFilmGuestSerializer(FilmGuestSerializer):
    class Meta(FilmGuestSerializer.Meta):
        fields = [
            *ListFilmSerializer,
        ].remove("is_favorite")


class PhotoFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoFilm
        fields = ["photo_film"]


class ActorSerializer(serializers.Serializer):
    class Meta:
        model = ActorModel
        fields = [
            "name",
            "surname",
            "patronymic",
            "photo",
        ]


class CountryFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmContentModel
        fields = ["country"]


class BaseDetailedSerializer(serializers.ModelSerializer, WatchMixin, SeeLateMixin):
    class Meta:
        fields = [
            "description",
            "trailer",
            "producer",
            "cadrs",
            "actors",
            "countries",
            "comments",
            "videos",
            "is_watched",
            "is_see_late",
        ]


class DetailedFilmSerializer(FilmSerializer):
    cadrs = PhotoFilmSerializer(many=True)
    actors = ActorSerializer(many=True)
    countries = CountryFilmSerializer(many=True)
    comments = CommentSerializer(many=True)
    videos = MediaSerializer(many=True)

    class Meta(FilmSerializer.Meta):
        fields = [
            *FilmSerializer.Meta.fields,
            *BaseDetailedSerializer.Meta.fields,
        ]


class DetailedFilmGuestSerializer(BaseDetailedSerializer, FilmGuestSerializer):
    is_watched = None
    is_see_late = None

    class Meta(DetailedFilmSerializer.Meta):
        fields = [
            *[field for field in BaseDetailedSerializer.Meta.fields if field not in ("is_watched", "is_see_late")],
            *FilmGuestSerializer.Meta.fields,
        ]


class AdminContentSerializer(DetailedFilmSerializer):
    data_added = serializers.DateTimeField()

    class Meta(DetailedFilmSerializer.Meta):
        fields = [
            *DetailedFilmSerializer.Meta.fields,
            "data_added",
        ]
