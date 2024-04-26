from django import forms
from django.db.models import TextChoices
from wagtail.blocks import MultipleChoiceBlock
from wagtail.blocks import StructBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from some_proj.blog.mixin import BlogGetApiRepresentationMixin
from some_proj.blog.snippets import SerialBlogModel


class SerialChooseBlock(TextChoices):
    display_name = "Название", "Название"
    display_poster = "Постер", "Постер"
    display_contries = "Страны", "Страны"
    display_genres = "Жанры", "Жанры"
    display_discription = "Описание", "Описание"
    display_trailer = "Трейлер", "Трейлер"
    display_cadrs = "Кадры", "Кадры"
    display_actors = "Актёры", "Актёры"
    display_duration = "Длительность", "Длительность"
    display_director = "Режиссёр", "Режиссёр"
    display_season = "Сезон", "Сезон"
    display_num_serials = "Количество серий", "Количество серий"


class SerialBlog(BlogGetApiRepresentationMixin, StructBlock):
    serial = SnippetChooserBlock(
        SerialBlogModel,
        label="Выберите сериал",
    )
    serial_fields = MultipleChoiceBlock(
        choices=SerialChooseBlock.choices,
        label="Выберите поле для отображения",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        label = "Сериал"
