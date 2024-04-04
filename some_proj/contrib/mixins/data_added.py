from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class DataAddedMixin(serializers.Serializer):
    data_added = serializers.SerializerMethodField()

    @extend_schema_field(str)
    def get_data_added(self, obj):
        return str(obj.data_added) if obj.data_added else ""
