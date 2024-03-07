from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from some_proj.films.models import FavoriteContent
from some_proj.films.models import IsContentWatch
from some_proj.films.models import SeeLateContent
from some_proj.media_for_kino_card.models import MediaFile


class FavoriteMixin:
    is_favorite = serializers.SerializerMethodField()

    def get_is_favorite(self, obj):
        request = self.context.get("request")
        user = request.user
        return FavoriteContent.objects.filter(
            content_object=obj,
            user=user,
        ).exists()


class WatchMixin:
    is_watched = serializers.SerializerMethodField()

    def get_is_watched(self, obj):
        request = self.context.get("request")
        user = request.user
        content_type = ContentType.objects.get_for_model(obj)
        media = MediaFile.objects.get(content_type=content_type, object_id=obj.id)
        return IsContentWatch.objects.filter(
            content_object=obj,
            media=media,
            user=user,
        ).exists()


class SeeLateMixin:
    is_see_late = serializers.SerializerMethodField()

    def get_see_late(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return SeeLateContent.objects.filter(
            content_object=obj,
            user=user,
        ).exists()
