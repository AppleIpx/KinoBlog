from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class WatchMixin(serializers.Serializer):
    is_watched = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField)
    def get_is_watched(self, obj):
        return obj.is_watched
