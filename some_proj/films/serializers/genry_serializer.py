from rest_framework import serializers

from some_proj.films.models import GenreModel


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreModel
        fields = [
            "id",
            "name",
        ]
