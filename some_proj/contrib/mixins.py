from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from some_proj.comments.models import CommentModel
from some_proj.comments.serializers import CommentSerializer
from some_proj.films.models import FavoriteContent
from some_proj.films.models import IsContentWatch
from some_proj.films.models import SeeLateContent
from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.models import UrlsInMedia
from some_proj.media_for_kino_card.serializers import DataMediaSerializer
from some_proj.media_for_kino_card.serializers import UrlsInMediaSerializer


class FavoriteMixin:
    @extend_schema_field(bool)
    def get_is_favorite(self, obj):
        user = self.context.get("request").user
        content_type = ContentType.objects.get_for_model(obj)
        return FavoriteContent.objects.filter(
            content_type=content_type,
            object_id=obj.pk,
            user=user,
        ).exists()


class WatchMixin:
    is_watched = serializers.SerializerMethodField()

    @extend_schema_field(bool)
    def get_is_watched(self, obj):
        user = self.context.get("request").user
        content_type = ContentType.objects.get_for_model(obj)
        return IsContentWatch.objects.filter(
            object_id=obj.id,
            content_type=content_type,
            user=user,
        ).exists()


class SeeLateMixin:
    is_see_late = serializers.SerializerMethodField()

    @extend_schema_field(bool)
    def get_is_see_late(self, obj):
        user = self.context.get("request").user
        content_type = ContentType.objects.get_for_model(obj)
        return SeeLateContent.objects.filter(
            object_id=obj.id,
            content_type=content_type,
            user=user,
        ).exists()


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
        content_type = ContentType.objects.get_for_model(obj)
        media_files = MediaFile.objects.filter(content_type=content_type, object_id=obj.id)
        urls = UrlsInMedia.objects.filter(media__in=media_files)
        return UrlsInMediaSerializer(urls, many=True).data


class DataAddedMixin:
    data_added = serializers.SerializerMethodField()

    @extend_schema_field(str)
    def get_data_added(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        media_files = MediaFile.objects.filter(content_type=content_type, object_id=obj.id).first()
        serialized_data = DataMediaSerializer(media_files).data

        if serialized_data:
            data_added_value = serialized_data.get("data_added", "")
            return str(data_added_value)
        return ""
