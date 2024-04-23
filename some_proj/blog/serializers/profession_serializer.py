from rest_framework import serializers

from some_proj.blog.snippets.author_snippet import Profession


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = [
            "id",
            "name",
        ]
