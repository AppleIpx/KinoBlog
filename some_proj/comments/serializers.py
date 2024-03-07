from rest_framework import serializers

from some_proj.comments.models import CommentModel
from some_proj.users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CommentModel
        fields = [
            "id",
            "user",
            "text",
            "created_at",
        ]
