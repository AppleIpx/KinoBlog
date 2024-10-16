from rest_framework import serializers

from some_proj.contrib.mixins import DataAddedMixin
from some_proj.contrib.mixins import FavoriteMixin
from some_proj.contrib.mixins import GetPostersMixin
from some_proj.contrib.mixins import ReactionCountMixin
from some_proj.films.serializers.film_serializers import DetailedContentSerializer
from some_proj.serials.models import PhotoSerial
from some_proj.serials.models import SerialModel


class SerialSerializer(
    FavoriteMixin,
    GetPostersMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = SerialModel
        fields = [
            "id",
            "name",
            "release_date",
            "poster",
            "posters",
            "is_favorite",
            "season",
            "num_serials",
        ]


class ListSerialSerializer(
    SerialSerializer,
    ReactionCountMixin,
):
    class Meta(SerialSerializer.Meta):
        fields = [
            *SerialSerializer.Meta.fields,
            "duration",
            "like_count",
            "dislike_count",
            "age_limit",
        ]


class SerialGuestSerializer(SerialSerializer):
    class Meta(SerialSerializer.Meta):
        fields = [
            field
            for field in ListSerialSerializer.Meta.fields
            if field
            not in [
                "is_favorite",
                "like_count",
                "dislike_count",
            ]
        ]


class ListSerialGuestSerializer(SerialGuestSerializer):
    class Meta(SerialGuestSerializer.Meta):
        fields = [
            *SerialGuestSerializer.Meta.fields,
        ]


class CadrsSerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoSerial
        fields = [
            "id",
            "photo_serial",
        ]


class DetailedSerialSerializer(
    DetailedContentSerializer,
    ListSerialSerializer,
):
    cadrs = CadrsSerialSerializer(many=True)

    class Meta(ListSerialSerializer.Meta):
        fields = [
            *ListSerialSerializer.Meta.fields,
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


class DetailedSerialGuestSerializer(
    DetailedSerialSerializer,
    SerialGuestSerializer,
):
    class Meta(SerialGuestSerializer.Meta):
        fields = [
            *[
                field
                for field in DetailedSerialSerializer.Meta.fields
                if field
                not in [
                    "is_watched",
                    "is_see_late",
                    "is_favorite",
                    "like_count",
                    "dislike_count",
                ]
            ],
            *SerialGuestSerializer.Meta.fields,
        ]


class AdminSerialSerializer(DataAddedMixin, DetailedSerialSerializer):
    class Meta(DetailedSerialSerializer.Meta):
        fields = [
            *DetailedSerialSerializer.Meta.fields,
            "data_added",
        ]


class AdminListSerialSerializer(DataAddedMixin, ListSerialSerializer):
    class Meta(SerialSerializer.Meta):
        fields = [
            *ListSerialSerializer.Meta.fields,
            "data_added",
        ]
