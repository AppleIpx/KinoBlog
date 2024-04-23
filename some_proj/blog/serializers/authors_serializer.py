from rest_framework import serializers

from some_proj.blog.snippets.author_snippet import AuthorBlog


class AuthorBlogSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    author_image = serializers.ImageField(required=False)

    class Meta:
        model = AuthorBlog
        fields = [
            "id",
            "first_name",
            "last_name",
            "author_email",
            "author_image",
        ]
