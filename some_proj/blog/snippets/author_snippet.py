from django.contrib.auth import get_user_model
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

User = get_user_model()


@register_snippet
class Profession(models.Model):
    name = models.CharField(
        max_length=155,
        verbose_name="Профессия",
        help_text="Название профессии",
    )
    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        verbose_name = "профессия"
        verbose_name_plural = "профессии"

    def __str__(self):
        return self.name


@register_snippet
class AuthorBlog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Выберите пользователя",
    )
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
        "blog.CustomImage",
        verbose_name="Изображение автора",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    profession = models.ManyToManyField(
        Profession,
        verbose_name="Профессия",
        help_text="Выберите профессию",
        blank=True,
    )
    panels = [
        FieldPanel("user"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("author_email"),
        FieldPanel("profession"),
        FieldPanel("author_image"),
    ]

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
