from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField

from some_proj.blog.serializers.tags_serializer import BlogTagPageSerializer


class ImageBlockSerializer(serializers.Field):
    url = serializers.URLField(required=False)
    full_url = serializers.URLField(required=False)
    width = serializers.IntegerField(required=False)
    height = serializers.IntegerField(required=False)
    alt = serializers.CharField(required=False)
    tags = BlogTagPageSerializer(many=True, required=False)

    def to_representation(self, instance):
        if instance.file:
            return {
                "image": ImageRenditionField("max-1920x1080|format-jpeg").to_representation(instance),
                "image_tags": [{"id": tag.id, "name": tag.name} for tag in instance.tags.all()],
            }
        return None
