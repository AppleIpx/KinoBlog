from rest_framework import serializers

from some_proj.films.models import PhotoFilm


class CadrsFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoFilm
        fields = [
            "id",
            "photo_film",
        ]
        fields_to_process = ["photo_film"]
