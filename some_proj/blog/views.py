from django.db.models import Prefetch
from rest_framework import mixins
from rest_framework import viewsets

from some_proj.blog.models import BlogPage
from some_proj.blog.serializers.blog_serializer import DetailBlogSerializer
from some_proj.blog.serializers.blog_serializer import ListBlogSerializer
from some_proj.blog.snippets.author_snippet import AuthorBlog


class BlockPageView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_mapping = {
        "list": ListBlogSerializer,
        "detailed": DetailBlogSerializer,
    }

    def get_serializer_class(self):
        has_pk_param = bool(self.kwargs.get("pk"))
        if has_pk_param:
            self.action = "detailed"
        else:
            self.action = "list"
        return self.serializer_mapping[self.action]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        author_image_prefetch = Prefetch(
            "authors__author_image",
            queryset=AuthorBlog.objects.all(),
        )
        return BlogPage.objects.prefetch_related(
            "tags",
            "authors",
            author_image_prefetch,
        )
