from drf_spectacular.utils import extend_schema_field
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers

from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.models import UrlsInMedia


class UrlsMixin(serializers.Serializer):
    urls = serializers.SerializerMethodField()

    @extend_schema_field(
        inline_serializer(
            name="FieldData",
            fields={
                "quality": serializers.CharField(),
                "url_quality": serializers.CharField(),
            },
        ),
    )
    def get_urls(self, obj):
        media_files = MediaFile.objects.filter(
            content_type=obj.content_type,
            object_id=obj.id,
        ).select_related("media")
        urls = UrlsInMedia.objects.filter(
            media__in=media_files,
        ).values("quality__name", "url", "id")
        return [{"id": url["id"], "quality": url["quality__name"], "url": url["url"]} for url in urls]
