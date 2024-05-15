from rest_framework import serializers

from some_proj.blog.models import BlogPage
from some_proj.blog.serializers.authors_serializer import AuthorBlogSerializer
from some_proj.blog.serializers.stream_field_serializer import StreamFieldSerializer
from some_proj.blog.serializers.tags_serializer import BlogTagPageSerializer


class ListBlogSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%A %d %B %Y")
    tags = BlogTagPageSerializer(source="tagged_items", many=True)
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

    class Meta(ListBlogSerializer.Meta):
        fields = [
            *ListBlogSerializer.Meta.fields,
            "body",
        ]
