from rest_framework import serializers

from some_proj.blog.models import BlogTagPage


class BlogTagPageSerializer(serializers.ModelSerializer):
    tag_name = serializers.SlugRelatedField(
        source="tag",
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = BlogTagPage
        fields = [
            "id",
            "tag_name",
        ]
