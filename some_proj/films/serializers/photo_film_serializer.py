from rest_framework import serializers

from some_proj.films.models import PhotoFilm
from some_proj.media_for_kino_card.utils.shared_files import BaseHTTPRemoverSerializer


class PhotoFilmSerializer(BaseHTTPRemoverSerializer, serializers.ModelSerializer):
    class Meta:
        model = PhotoFilm
        fields = ["photo_film"]
        fields_to_process = ["photo_film"]
