from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from some_proj.comments.models import CommentModel
from some_proj.comments.serializers import CommentSerializer


class CommentMixin(serializers.Serializer):
    comments = serializers.SerializerMethodField()

    @extend_schema_field(CommentSerializer)
    def get_comments(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        comments_qs = CommentModel.objects.filter(
            object_id=obj.id,
            content_type=content_type,
        ).prefetch_related("user")

        serializer = CommentSerializer(comments_qs, many=True)

        return serializer.data
