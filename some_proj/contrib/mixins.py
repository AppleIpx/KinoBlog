from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from some_proj.comments.models import CommentModel
from some_proj.comments.serializers import CommentSerializer
from some_proj.media_for_kino_card.models import UrlsInMedia
from some_proj.media_for_kino_card.serializers import UrlsInMediaSerializer


class FavoriteMixin:
    @extend_schema_field(bool)
    def get_is_favorite(self, obj):
        return obj.is_favorite


class WatchMixin:
    @extend_schema_field(bool)
    def get_is_watched(self, obj):
        return obj.is_watched


class SeeLateMixin:
    @extend_schema_field(bool)
    def get_is_see_late(self, obj):
        return obj.is_see_late


class CommentMixin:
    comments = serializers.SerializerMethodField()

    @extend_schema_field(CommentSerializer)
    def get_comments(self, obj):
        comments_qs = CommentModel.objects.filter(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )
        serializer = CommentSerializer(comments_qs, many=True)
        return serializer.data


class ReationCountMixin:
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    @extend_schema_field(int)
    def get_like_count(self, obj):
        return obj.like_count

    @extend_schema_field(int)
    def get_dislike_count(self, obj):
        return obj.dislike_count


class GetPostersMixin:
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


class UrlsMixin:
    urls = serializers.SerializerMethodField()

    @extend_schema_field(UrlsInMediaSerializer)
    def get_urls(self, obj):
        media_files = getattr(obj, "media_files", None)
        if media_files is not None:
            prefetch_media = Prefetch("media", queryset=UrlsInMedia.objects.select_related("media"))
            media_files_with_urls = media_files.prefetch_related(prefetch_media)
            return UrlsInMediaSerializer(media_files_with_urls, many=True).data
        return []


class DataAddedMixin:
    data_added = serializers.SerializerMethodField()

    @extend_schema_field(str)
    def get_data_added(self, obj):
        return str(obj.data_added) if obj.data_added else ""
