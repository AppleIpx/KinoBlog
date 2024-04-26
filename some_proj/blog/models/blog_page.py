from django import forms
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from some_proj.blog.models.custom_image import CustomImageChoose
from some_proj.blog.models.film_blog import FilmBlog
from some_proj.blog.models.serial_blog import SerialBlog
from some_proj.blog.snippets.author_snippet import AuthorBlog


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
            ("images", CustomImageChoose()),
            (
                "content",
                EmbedBlock(
                    label="Ссылка на видео контент",
                    help_text="Пример ссылки: https://www.youtube.com/watch?v=5mM0fX_kKCU",
                ),
            ),
            ("film", FilmBlog()),
            ("serial", SerialBlog()),
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
    ]

    subpage_types = []
    parent_page_types = ["home.HomePage"]

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"
