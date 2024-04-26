from some_proj.blog.serializers.film_blog_serializer import FilmBlogSerializer
from some_proj.blog.serializers.serial_blog_serializer import SerialBlogSerializer
from some_proj.blog.snippets import FilmBlogModel
from some_proj.blog.snippets import SerialBlogModel


class BlogGetApiRepresentationMixin:
    CONTENT_DATA = {
        "film": {
            "model": FilmBlogModel,
            "serializer": FilmBlogSerializer,
        },
        "serial": {
            "model": SerialBlogModel,
            "serializer": SerialBlogSerializer,
        },
    }
    CONTENT_FIELDS = {
        "Название": "name",
        "Постер": "poster",
        "Страны": "country",
        "Жанры": "genre",
        "Описание": "description",
        "Трейлер": "trailer",
        "Кадры": "cadrs",
        "Актёры": "actors",
        "Длительность": "duration",
        "Режиссёр": "producers",
        "Сезон": "season",
        "Количество серий": "num_serials",
    }

    def get_api_representation(self, value, context=None):
        representation = super().get_api_representation(value, context)
        content_type = self.name
        if content_type_id := representation.get(f"{content_type}"):
            content_model = self.CONTENT_DATA[content_type]["model"].objects.get(id=content_type_id)
            fields = representation.get(f"{content_type}_fields")
            if fields:
                content_type_serialized = self.CONTENT_DATA[content_type]["serializer"](content_model).data
                selected_fields = {}
                for field_name in fields:
                    field_key = self.CONTENT_FIELDS.get(field_name)
                    if field_key in content_type_serialized:
                        selected_fields[field_key] = content_type_serialized[field_key]
                        representation = selected_fields
        return representation
