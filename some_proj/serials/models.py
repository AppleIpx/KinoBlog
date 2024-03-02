from django.db import models

from some_proj.films.models import BaseModel


class SerialModel(BaseModel):
    season = models.PositiveIntegerField(
        verbose_name="Сезон",
    )
    num_serials = models.PositiveIntegerField(
        verbose_name="Кол-во серий",
    )
    release_date = models.DateField(
        verbose_name="Дата выхода сериала",
    )

    class Meta:
        verbose_name = "Сериал"
        verbose_name_plural = "Сериалы"

    def __str__(self):
        return f"{self.name} {self.season} сезон"
