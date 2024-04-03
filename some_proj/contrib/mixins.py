from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from some_proj.comments.models import CommentModel
from some_proj.comments.serializers import CommentSerializer
from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.models import UrlsInMedia
from some_proj.media_for_kino_card.serializers import UrlsInMediaSerializer


class FavoriteMixin(serializers.Serializer):
    is_favorite = serializers.SerializerMethodField()

    @extend_schema_field(bool)
    def get_is_favorite(self, obj):
        return obj.is_favorite


class WatchMixin(serializers.Serializer):
    is_watched = serializers.SerializerMethodField()

    @extend_schema_field(bool)
    def get_is_watched(self, obj):
        return obj.is_watched


class SeeLateMixin(serializers.Serializer):
    is_see_late = serializers.SerializerMethodField()

    @extend_schema_field(bool)
    def get_is_see_late(self, obj):
        return obj.is_see_late


class CommentMixin(serializers.Serializer):
    comments = serializers.SerializerMethodField()

    @extend_schema_field(CommentSerializer)
    def get_comments(self, obj):
        content_type = ContentType.objects.get_for_model(obj)

        comments_qs = CommentModel.objects.filter(
            object_id=obj.id,
            content_type=content_type,
        ).prefetch_related("user")

        serializer = CommentSerializer(comments_qs, many=True)

        return serializer.data


class ReactionCountMixin(serializers.Serializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField)
    def get_like_count(self, obj):
        return obj.like_count

    @extend_schema_field(serializers.IntegerField)
    def get_dislike_count(self, obj):
        return obj.dislike_count


class GetPostersMixin(serializers.Serializer):
    posters = serializers.SerializerMethodField()

    @extend_schema_field(dict)
    def get_posters(self, obj):
        if obj.poster:
            low = get_thumbnail(
                obj.poster,
                geometry_string="360",
                crop="center",
                quality=99,
            )
            average = get_thumbnail(
                obj.poster,
                geometry_string="720",
                crop="center",
                quality=99,
            )
            high = get_thumbnail(
                obj.poster,
                geometry_string="1920",
                crop="center",
                quality=99,
            )
            return {
                "low": low.url,
                "average": average.url,
                "high": high.url,
            }
        return None


class UrlsMixin(serializers.Serializer):
    urls = serializers.SerializerMethodField()

    @extend_schema_field(UrlsInMediaSerializer)
    def get_urls(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        media_files = MediaFile.objects.filter(content_type=content_type, object_id=obj.id).select_related("media")
        urls = UrlsInMedia.objects.filter(media__in=media_files).values("quality__name", "url")
        return {url["quality__name"]: url["url"] for url in urls}


class DataAddedMixin(serializers.Serializer):
    data_added = serializers.SerializerMethodField()

    @extend_schema_field(str)
    def get_data_added(self, obj):
        return str(obj.data_added) if obj.data_added else ""
