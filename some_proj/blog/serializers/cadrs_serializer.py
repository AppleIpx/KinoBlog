from rest_framework import serializers

from some_proj.blog.snippets import CadrsModel
from some_proj.films.serializers import CadrsFilmSerializer
from some_proj.serials.serializers import PhotoSerialSerializer


class CadrsBlogSerializer(serializers.ModelSerializer):
    film_photos = CadrsFilmSerializer(many=True)
    serial_photos = PhotoSerialSerializer(many=True)

    class Meta:
        model = CadrsModel
        fields = [
            "film_photos",
            "serial_photos",
        ]
