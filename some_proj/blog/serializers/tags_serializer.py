from rest_framework import serializers

from some_proj.blog.models.blog_page import BlogTagPage


class BlogTagPageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="tag.id")
    tag_name = serializers.CharField(source="tag.name")

    class Meta:
        model = BlogTagPage
        fields = [
            "id",
            "tag_name",
        ]
