from django import forms
from django.db.models import TextChoices
from wagtail.blocks import MultipleChoiceBlock
from wagtail.blocks import StructBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from some_proj.blog.mixin import BlogGetApiRepresentationMixin
from some_proj.blog.snippets import FilmBlogModel


class FilmChooseBlock(TextChoices):
    display_name = "Название", "Название"
    display_poster = "Постер", "Постер"
    display_contries = "Страны", "Страны"
    display_genres = "Жанры", "Жанры"
    display_description = "Описание", "Описание"
    display_trailer = "Трейлер", "Трейлер"
    display_cadrs = "Кадры", "Кадры"
    display_actors = "Актёры", "Актёры"
    display_duration = "Длительность", "Длительность"
    display_director = "Режиссёр", "Режиссёр"


class FilmBlog(BlogGetApiRepresentationMixin, StructBlock):
    film = SnippetChooserBlock(
        FilmBlogModel,
        label="Выберите фильм",
    )
    film_fields = MultipleChoiceBlock(
        choices=FilmChooseBlock.choices,
        label="Выберите поле для отображения",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        label = "Фильм"
