from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class ReactionCountMixin(serializers.Serializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField)
    def get_like_count(self, obj):
        return obj.like_count

    @extend_schema_field(serializers.IntegerField)
    def get_dislike_count(self, obj):
        return obj.dislike_count
