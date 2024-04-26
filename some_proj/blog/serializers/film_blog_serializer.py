from some_proj.blog.snippets.film_snippet import DefaultFields
from some_proj.films.models import FilmModel
from some_proj.films.serializers import CadrsFilmSerializer
from some_proj.films.serializers.film_serializers import DetailedContentSerializer


class FilmBlogSerializer(DetailedContentSerializer):
    cadrs = CadrsFilmSerializer(many=True)

    class Meta:
        model = FilmModel
        fields = [
            *DefaultFields,
        ]
        fields_to_process = ["poster"]
