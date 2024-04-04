from drf_spectacular.utils import extend_schema_field
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework.fields import CharField
from sorl.thumbnail import get_thumbnail


class GetPostersMixin(serializers.Serializer):
    posters = serializers.SerializerMethodField()

    # @extend_schema_field(dict)
    @extend_schema_field(
        inline_serializer(
            name="PostersFieldData",
            fields={
                "size": CharField(),
                "url_size": CharField(),
            },
        ),
    )
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
                "size_low": "low",
                "url_low": low.url,
                "size_average": "average",
                "url_average": average.url,
                "size_high": "high",
                "url_high": high.url,
            }
        return None
