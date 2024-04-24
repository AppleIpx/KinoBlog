from some_proj.blog.snippets import FilmBlogModel
from some_proj.blog.snippets.film_snippet import DefaultFields
from some_proj.films.serializers.film_serializers import DetailedContentSerializer


class WidgetFilmBlogSerializer(DetailedContentSerializer):
    class Meta:
        model = FilmBlogModel
        fields = [
            *DefaultFields,
        ]
        fields_to_process = ["poster"]
