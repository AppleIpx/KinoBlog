from django.contrib.auth import get_user_model
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from some_proj.blog.models import BlogPage

User = get_user_model()


@register_snippet
class AuthorBlog(User):
    first_name = models.CharField(
        max_length=250,
        verbose_name="Имя",
        blank=True,
    )
    last_name = models.CharField(
        max_length=250,
        verbose_name="Фамилия",
        blank=True,
    )
    author_email = models.EmailField(
        verbose_name="Электронная почтв",
        blank=True,
    )
    author_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Изображение автора",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    block_post = ParentalKey(
        BlogPage,
        on_delete=models.CASCADE,
        related_name="authors",
    )
    panels = [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("author_email"),
        FieldPanel("author_image"),
        FieldPanel("block_post"),
    ]

    def __str__(self):
        return f"{self.name} {self.last_name}"
