from some_proj.blog.snippets.film_snippet import DefaultFields
from some_proj.films.serializers.film_serializers import DetailedContentSerializer
from some_proj.serials.models import SerialModel
from some_proj.serials.serializers import CadrsSerialSerializer


class SerialBlogSerializer(DetailedContentSerializer):
    cadrs = CadrsSerialSerializer(many=True)

    class Meta:
        model = SerialModel
        fields = [
            *DefaultFields,
            "season",
            "num_serials",
        ]
        fields_to_process = ["poster"]
