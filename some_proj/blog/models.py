from django import forms
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import InlinePanel
from wagtail.blocks import RichTextBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock

from some_proj.blog.snippets import FilmBlogModel
from some_proj.blog.snippets import SerialBlogModel
from some_proj.blog.snippets import SlidesModel
from some_proj.blog.snippets.author_snippet import AuthorBlog
from some_proj.media_for_kino_card.utils.shared_files import generate_filename_photos


class BlogTagPage(TaggedItemBase):
    content_object = ParentalKey(
        "blog.BlogPage",
        on_delete=models.CASCADE,
        related_name="tags",
    )


class BlogPage(Page):
    date = models.DateField("Дата публикации")
    tag = ClusterTaggableManager(
        through=BlogTagPage,
        blank=True,
    )
    authors = ParentalManyToManyField(
        AuthorBlog,
        verbose_name="Автор",
        blank=True,
    )
    body = StreamField(
        [
            (
                "text",
                RichTextBlock(
                    features=["h1", "h2", "h3", "bold", "italic", "hr", "blockquote"],
                    label="Текст",
                    help_text="Введите описание",
                ),
            ),
            (
                "image",
                ImageChooserBlock(
                    template="blocks/imgblock.html",
                    label="Изображение",
                    icon="image",
                    help_text="Загрузите изображение",
                    upload_to=generate_filename_photos,
                ),
            ),
            (
                "content",
                EmbedBlock(
                    label="Ссылка на видео контент",
                    help_text="Пример ссылки: https://www.youtube.com/watch?v=5mM0fX_kKCU",
                ),
            ),
            (
                "film",
                SnippetChooserBlock(
                    FilmBlogModel,
                    label="Фильм",
                    required=False,
                    help_text="Укажите фильм",
                ),
            ),
            (
                "serial",
                SnippetChooserBlock(
                    SerialBlogModel,
                    label="Сериал",
                    required=False,
                    help_text="Укажите сериал",
                ),
            ),
            (
                "slides",
                SnippetChooserBlock(
                    SlidesModel,
                    label="Кадры из фильма/сериала",
                    required=False,
                ),
            ),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Место для творчества",
    )
    search_fields = [
        *Page.search_fields,
        index.SearchField("title"),
        index.SearchField("body"),
        index.SearchField("tag"),
    ]

    content_panels = [
        *Page.content_panels,
        FieldPanel("title"),
        FieldPanel("date"),
        FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
        FieldPanel("tag"),
        FieldPanel("body"),
        InlinePanel("slides", label="слайд"),
    ]

    subpage_types = []
    parent_page_types = ["home.HomePage"]

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"


class BlockImages(Orderable):
    caption = models.CharField(
        max_length=250,
        verbose_name="Текст слайда",
        blank=True,
    )
    figure = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Картинка",
        blank=True,
        null=True,
    )
    blog = ParentalKey(
        BlogPage,
        related_name="slides",
        on_delete=models.CASCADE,
    )
