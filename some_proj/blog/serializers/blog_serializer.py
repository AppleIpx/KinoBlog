from rest_framework import serializers

from some_proj.blog.models import BlogPage
from some_proj.blog.serializers import AuthorBlogSerializer
from some_proj.blog.serializers import BlogTagPageSerializer
from some_proj.blog.serializers.stream_field_serializer import StreamFieldSerializer


class ListBlogSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%A %d %B %Y")
    tags = BlogTagPageSerializer(source="tags.all", many=True)
    authors = AuthorBlogSerializer(many=True)

    class Meta:
        model = BlogPage
        fields = [
            "id",
            "date",
            "authors",
            "title",
            "tags",
        ]


class DetailBlogSerializer(ListBlogSerializer):
    body = StreamFieldSerializer()
    slides = serializers.SerializerMethodField()

    def get_slides(self, obj):
        pass

    class Meta(ListBlogSerializer.Meta):
        fields = [
            *ListBlogSerializer.Meta.fields,
            "body",
            "slides",
        ]
