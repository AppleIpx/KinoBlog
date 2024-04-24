from django.db import models
from django.db.models import ManyToManyField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from some_proj.blog.utils.cadrs_check_content import cadrs_check
from some_proj.films.models import PhotoFilm
from some_proj.serials.models import PhotoSerial


@register_snippet
class CadrsModel(models.Model):
    film_photos = ManyToManyField(
        PhotoFilm,
        blank=True,
    )
    serial_photos = ManyToManyField(
        PhotoSerial,
        blank=True,
    )
    panels = [
        FieldPanel("film_photos"),
        FieldPanel("serial_photos"),
    ]

    class Meta:
        verbose_name = "кадр с фильма/сериала"
        verbose_name_plural = "кадры с фильмов/сериалов"

    def __str__(self):
        return cadrs_check(self.film_photos, self.serial_photos)
