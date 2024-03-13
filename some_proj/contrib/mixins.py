from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

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
    def get_is_favorite(self, obj):
        request = self.context.get("request")
        user = request.user
        content_type = ContentType.objects.get_for_model(obj)
        return FavoriteContent.objects.filter(
            content_type=content_type,
            object_id=obj.pk,
            user=user,
        ).exists()


class WatchMixin:
    is_watched = serializers.SerializerMethodField()

    def get_is_watched(self, obj):
        request = self.context.get("request")
        user = request.user
        content_type = ContentType.objects.get_for_model(obj)
        return IsContentWatch.objects.filter(
            object_id=obj.id,
            content_type=content_type,
            user=user,
        ).exists()


class SeeLateMixin:
    is_see_late = serializers.SerializerMethodField()

    def get_is_see_late(self, obj):
        request = self.context.get("request")
        user = request.user
        content_type = ContentType.objects.get_for_model(obj)
        return SeeLateContent.objects.filter(
            object_id=obj.id,
            content_type=content_type,
            user=user,
        ).exists()


class CommentMixin:
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments_qs = CommentModel.objects.filter(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )
        serializer = CommentSerializer(comments_qs, many=True)
        return serializer.data


class CountLikeMixin:
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.like_count


class CountDislikeMixin:
    dislike_count = serializers.SerializerMethodField()

    def get_dislike_count(self, obj):
        return obj.dislike_count


class UrlsMixin:
    urls = serializers.SerializerMethodField()

    def get_urls(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        media_files = MediaFile.objects.filter(content_type=content_type, object_id=obj.id)
        urls = UrlsInMedia.objects.filter(media__in=media_files)

        # Сериализуем данные и возвращаем .data
        return UrlsInMediaSerializer(urls, many=True).data


class DataAddedMixin:
    data_added = serializers.SerializerMethodField()

    def get_data_added(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        media_files = MediaFile.objects.filter(content_type=content_type, object_id=obj.id).first()
        return DataMediaSerializer(media_files).data
