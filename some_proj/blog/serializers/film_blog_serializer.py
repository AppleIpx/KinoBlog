from rest_framework import serializers

from some_proj.blog.snippets.film_snippet import DefaultFields
from some_proj.films.models import FilmModel
from some_proj.films.serializers import ActorSerializer
from some_proj.films.serializers import CadrsFilmSerializer
from some_proj.films.serializers import CountrySerializer
from some_proj.films.serializers import GenreSerializer
from some_proj.films.serializers import ProducerSerializer


class FilmBlogSerializer(serializers.ModelSerializer):
    cadrs = CadrsFilmSerializer(many=True)
    actors = ActorSerializer(many=True)
    producers = ProducerSerializer(many=True)
    country = CountrySerializer(many=True)
    genre = GenreSerializer(many=True)

    class Meta:
        model = FilmModel
        fields = [
            *DefaultFields,
            "poster",
        ]
