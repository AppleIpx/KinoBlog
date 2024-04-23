from rest_framework import serializers

from some_proj.blog.snippets.films_cadrs_snippet import FilmsCadrsModel


class FilmsCadrsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmsCadrsModel
        fields = [
            "film",
            "photo_film",
        ]
