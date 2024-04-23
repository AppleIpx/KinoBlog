from rest_framework import serializers


class EmbedBlockSerializer(serializers.Serializer):
    url = serializers.CharField()

    def to_representation(self, instance):
        return {
            "url": instance.url,
        }

    def to_internal_value(self, data):
        return {
            "url": data.get("url"),
        }
