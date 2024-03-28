from rest_framework import serializers

from some_proj.contrib.mixins import CommentMixin
from some_proj.contrib.mixins import DataAddedMixin
from some_proj.contrib.mixins import FavoriteMixin
from some_proj.contrib.mixins import GetPostersMixin
from some_proj.contrib.mixins import ReationCountMixin
from some_proj.contrib.mixins import SeeLateMixin
from some_proj.contrib.mixins import UrlsMixin
from some_proj.contrib.mixins import WatchMixin
from some_proj.films.models import FilmModel
from some_proj.films.serializers import ActorSerializer
from some_proj.films.serializers import CadrsFilmSerializer
from some_proj.films.serializers import CountrySerializer
from some_proj.films.serializers import GenreSerializer
from some_proj.films.serializers import ProducerSerializer
from some_proj.media_for_kino_card.utils.shared_files import HTTPRemoverSerializer


class FilmsSerializer(
    FavoriteMixin,
    GetPostersMixin,
    HTTPRemoverSerializer,
    serializers.ModelSerializer,
):
    is_favorite = serializers.SerializerMethodField()
    posters = serializers.SerializerMethodField()

    class Meta:
        model = FilmModel
        fields = [
            "id",
            "poster",
            "posters",
            "name",
            "release_date",
            "duration",
            "is_favorite",
            "age_limit",
        ]
        fields_to_process = [
            "poster",
            "posters",
        ]


class ListFilmSerializer(
    ReationCountMixin,
    FilmsSerializer,
):
    dislike_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta(FilmsSerializer.Meta):
        fields = [
            *FilmsSerializer.Meta.fields,
            "dislike_count",
            "like_count",
        ]


class FilmGuestSerializer(FilmsSerializer):
    is_favorite = None

    class Meta(ListFilmSerializer.Meta):
        fields = [
            field
            for field in ListFilmSerializer.Meta.fields
            if field
            not in [
                "is_favorite",
            ]
        ]


class ListFilmGuestSerializer(FilmGuestSerializer):
    class Meta(FilmGuestSerializer.Meta):
        fields = [
            *FilmGuestSerializer.Meta.fields,
        ]


class DetailedContentSerializer(
    HTTPRemoverSerializer,
    WatchMixin,
    SeeLateMixin,
    CommentMixin,
    UrlsMixin,
    serializers.Serializer,
):
    actors = ActorSerializer(many=True)
    producers = ProducerSerializer(many=True)
    country = CountrySerializer(many=True)
    genre = GenreSerializer(many=True)
    comments = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField()
    is_watched = serializers.SerializerMethodField()
    is_see_late = serializers.SerializerMethodField()


class DetailedFilmSerializer(
    DetailedContentSerializer,
    ListFilmSerializer,
):
    cadrs = CadrsFilmSerializer(many=True)

    class Meta(ListFilmSerializer.Meta):
        fields = [
            *ListFilmSerializer.Meta.fields,
            "is_watched",
            "is_see_late",
            "description",
            "trailer",
            "producers",
            "cadrs",
            "actors",
            "country",
            "genre",
            "comments",
            "urls",
        ]


class DetailedFilmGuestSerializer(DetailedFilmSerializer, FilmGuestSerializer):
    is_watched = None
    is_see_late = None

    class Meta(DetailedFilmSerializer.Meta):
        fields = [
            *[
                field
                for field in DetailedFilmSerializer.Meta.fields
                if field
                not in [
                    "is_watched",
                    "is_see_late",
                    "is_favorite",
                ]
            ],
            *FilmGuestSerializer.Meta.fields,
        ]


class AdminFilmSerializer(DataAddedMixin, DetailedFilmSerializer):
    data_added = serializers.SerializerMethodField()

    class Meta(DetailedFilmSerializer.Meta):
        fields = [
            *DetailedFilmSerializer.Meta.fields,
            "data_added",
        ]


class AdminListFilmSerializer(DataAddedMixin, ListFilmSerializer):
    data_added = serializers.SerializerMethodField()

    class Meta(FilmsSerializer.Meta):
        fields = [
            *ListFilmSerializer.Meta.fields,
            "data_added",
        ]
