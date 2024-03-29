from rest_framework import serializers

from some_proj.contrib.mixins import DataAddedMixin
from some_proj.contrib.mixins import FavoriteMixin
from some_proj.contrib.mixins import ReationCountMixin
from some_proj.films.serializers.film_serializers import DetailedContentSerializer
from some_proj.media_for_kino_card.utils.shared_files import HTTPRemoverSerializer
from some_proj.serials.models import PhotoSerial
from some_proj.serials.models import SerialModel


class SerialSerializer(
    FavoriteMixin,
    HTTPRemoverSerializer,
    serializers.ModelSerializer,
):
    poster = serializers.ImageField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = SerialModel
        fields = [
            "id",
            "name",
            "release_date",
            "poster",
            "is_favorite",
            "season",
            "num_serials",
        ]
        fields_to_process = ["poster"]


class ListSerialSerializer(
    SerialSerializer,
    ReationCountMixin,
):
    dislike_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta(SerialSerializer.Meta):
        fields = [
            *SerialSerializer.Meta.fields,
            "duration",
            "like_count",
            "dislike_count",
            "age_limit",
        ]


class SerialGuestSerializer(SerialSerializer):
    is_favorite = None

    class Meta(SerialSerializer.Meta):
        fields = [
            field
            for field in ListSerialSerializer.Meta.fields
            if field
            not in [
                "is_favorite",
            ]
        ]


class ListSerialGuestSerializer(SerialGuestSerializer):
    class Meta(SerialGuestSerializer.Meta):
        fields = [
            *SerialGuestSerializer.Meta.fields,
        ]


class AdminListSerialSerializer(DataAddedMixin, ListSerialSerializer):
    data_added = serializers.SerializerMethodField()

    class Meta(SerialSerializer.Meta):
        fields = [
            *ListSerialSerializer.Meta.fields,
            "data_added",
        ]


class PhotoSerialSerializer(serializers.ModelSerializer):
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
    cadrs = PhotoSerialSerializer(many=True)

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
    is_watched = None
    is_see_late = None

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
                ]
            ],
            *SerialGuestSerializer.Meta.fields,
        ]


class AdminSerialSerializer(DataAddedMixin, DetailedSerialSerializer):
    data_added = serializers.SerializerMethodField()

    class Meta(DetailedSerialSerializer.Meta):
        fields = [
            *DetailedSerialSerializer.Meta.fields,
            "data_added",
        ]
