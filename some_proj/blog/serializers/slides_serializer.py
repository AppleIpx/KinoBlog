from rest_framework import serializers

from some_proj.blog.snippets import SlidesModel


class SliderBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlidesModel
        fields = [
            "film_photos",
            "serial_photos",
        ]
