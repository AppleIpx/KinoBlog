from rest_framework import serializers

from some_proj.blog.serializers.profession_serializer import ProfessionSerializer
from some_proj.blog.snippets.author_snippet import AuthorBlog
from some_proj.users.serializers import UserSerializer


class AuthorBlogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    author_email = serializers.EmailField(read_only=True)
    author_image = serializers.ImageField(required=False)
    profession = ProfessionSerializer(many=True)

    class Meta:
        model = AuthorBlog
        fields = [
            "id",
            "first_name",
            "last_name",
            "user",
            "profession",
            "author_email",
            "author_image",
        ]
