from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from some_proj.films.models import PhotoFilm


@register_snippet
class FilmsCadrsModel(PhotoFilm):
    panels = [
        FieldPanel("film"),
        FieldPanel("photo_film"),
    ]

    class Meta:
        verbose_name = "кадр из фильма"
        verbose_name_plural = "кадры из фильмов"
        proxy = True

    def __str__(self):
        return f"кадр из {self.film.name}"
