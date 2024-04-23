from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from some_proj.films.models import FilmModel

DefaultPanels = [
    FieldPanel("name"),
    FieldPanel("poster"),
    FieldPanel("description"),
    FieldPanel("age_limit"),
    FieldPanel("country"),
    FieldPanel("producers"),
    FieldPanel("genre"),
    FieldPanel("actors"),
    FieldPanel("duration"),
    FieldPanel("release_date"),
]

DefaultFields = [
    "name",
    "poster",
    "age_limit",
    "country",
    "genre",
    "duration",
    "release_date",
]


@register_snippet
class FilmBlogModel(FilmModel):
    panels = [
        *DefaultPanels,
    ]

    class Meta:
        verbose_name = "фильм"
        verbose_name_plural = "фильмы"
        proxy = True

    def __str__(self):
        return f"{self.name}"
