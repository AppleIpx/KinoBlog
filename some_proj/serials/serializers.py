from rest_framework import serializers

from some_proj.comments.serializers import CommentSerializer
from some_proj.films.serializers import ActorSerializer
from some_proj.films.serializers import BaseDetailedSerializer
from some_proj.films.serializers import BaseSerializer
from some_proj.films.serializers import DetailedFilmSerializer
from some_proj.media_for_kino_card.serializers import MediaSerializer
from some_proj.serials.models import PhotoSerial
from some_proj.serials.models import SerialModel


class SerialSerializer(BaseSerializer):
    class Meta:
        model = SerialModel
        fields = [
            "id",
            "name",
            "release_date",
            "age_limit",
            "poster",
            "is_favorite",
            "season",
            "num_serials",
        ]


class SerialGuestSerializer(SerialSerializer):
    is_favorite = None

    class Meta(SerialSerializer.Meta):
        fields = [
            *SerialSerializer.Meta.fields,
        ].remove("is_favorite")


class ListSerialSerializer(SerialSerializer):
    class Meta(SerialSerializer.Meta):
        fields = [
            *SerialSerializer.Meta.fields,
            "duration",
            "genre",
            "reaction_like",
            "reaction_dislike",
        ]


class ListSerialGuestSerializer(SerialGuestSerializer):
    is_favorite = None

    class Meta(ListSerialSerializer.Meta):
        fields = [
            *ListSerialSerializer,
        ].remove("is_favorite")


class PhotoSerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoSerial
        fields = ["photo_serial"]


class CountrySerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialModel
        fields = ["country"]


class DetailedSerialSerializer(BaseDetailedSerializer, SerialSerializer):
    cadrs = PhotoSerialSerializer(many=True)
    actors = ActorSerializer(many=True)
    countries = CountrySerialSerializer(many=True)
    comments = CommentSerializer(many=True)
    videos = MediaSerializer(many=True)

    class Meta(SerialSerializer.Meta):
        fields = [
            *SerialSerializer.Meta.fields,
            *BaseDetailedSerializer,
        ]


class DetailedSerialGuestSerializer(BaseDetailedSerializer, SerialGuestSerializer):
    is_watched = None
    is_see_late = None

    class Meta(SerialGuestSerializer.Meta):
        fields = [
            *[field for field in BaseDetailedSerializer.Meta.fields if field not in ("is_watched", "is_see_late")],
            *SerialGuestSerializer.Meta.fields,
        ]


class AdminContentSerializer(DetailedSerialSerializer):
    data_added = serializers.DateTimeField()

    class Meta(DetailedFilmSerializer.Meta):
        fields = [
            *DetailedSerialSerializer.Meta.fields,
            "data_added",
        ]
