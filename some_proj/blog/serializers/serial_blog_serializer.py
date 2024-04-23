from some_proj.blog.snippets import SerialBlogModel
from some_proj.blog.snippets.film_snippet import DefaultFields
from some_proj.films.serializers.film_serializers import DetailedContentSerializer


class WidgetSerialBlogSerializer(DetailedContentSerializer):
    class Meta:
        model = SerialBlogModel
        fields = [
            *DefaultFields,
            "season",
            "num_serials",
        ]
