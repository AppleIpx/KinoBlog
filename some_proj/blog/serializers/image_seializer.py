from rest_framework import serializers
from wagtail.images.models import Image

from some_proj.contrib.mixins.add_bucket_in_url import AddBucketMixin
from some_proj.contrib.mixins.delete_http_in_url import DeleteHttpInUrlMixin


class CustomImageBlockSerializer(
    AddBucketMixin,
    DeleteHttpInUrlMixin,
    serializers.Serializer,
):
    image_url = serializers.URLField()

    def to_representation(self, instance):
        try:
            image_url = instance.file.url
            image_url = self.delete_http_in_url(image_url)
            image_url = self.add_bucket_name(image_url, "original_images")
        except Image.DoesNotExist:
            return {"image": None}
        else:
            return {"image": image_url}
