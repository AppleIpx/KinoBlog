from rest_framework import serializers

from some_proj.films.models import PhotoFilm


class PhotoFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoFilm
        fields = ["photo_film"]
