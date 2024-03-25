from rest_framework import serializers

from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.models import UrlsInMedia


class UrlsInMediaSerializer(serializers.ModelSerializer):
    quality = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = UrlsInMedia
        fields = [
            "quality",
            "url",
        ]


class MediaSerializer(serializers.ModelSerializer):
    urls = UrlsInMediaSerializer(many=True)

    class Meta:
        model = MediaFile
        fields = [
            "id",
            "episode",
            "data_added",
            "urls",
        ]


class DataMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = [
            "data_added",
        ]
