from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class SeeLateMixin(serializers.Serializer):
    is_see_late = serializers.SerializerMethodField()

    @extend_schema_field(bool)
    def get_is_see_late(self, obj):
        return obj.is_see_late
