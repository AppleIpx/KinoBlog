from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class FavoriteMixin(serializers.Serializer):
    is_favorite = serializers.SerializerMethodField()

    @extend_schema_field(bool)
    def get_is_favorite(self, obj):
        return obj.is_favorite
