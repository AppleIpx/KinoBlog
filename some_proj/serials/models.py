from django.contrib.auth import get_user_model
from django.db import models

from some_proj.films.models import BaseContentModel
from some_proj.media_for_kino_card.utils.shared_files import generate_filename_photos

User = get_user_model()


class SerialModel(BaseContentModel):
    season = models.PositiveSmallIntegerField(
        verbose_name="Сезон",
    )
    num_serials = models.PositiveSmallIntegerField(
        verbose_name="Кол-во серий",
    )
    release_date = models.DateField(
        verbose_name="Дата выхода сериала",
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name="Длительность серии",
    )

    class Meta:
        verbose_name = "сериал"
        verbose_name_plural = "сериалы"

    def __str__(self):
        return f"{self.name} {self.season} сезон"


class PhotoSerial(models.Model):
    serial = models.ForeignKey(
        SerialModel,
        verbose_name="Сериал",
        on_delete=models.CASCADE,
        related_name="cadrs",
    )
    photo_serial = models.ImageField(
        upload_to=generate_filename_photos,
        verbose_name="Кадр из сериала",
    )

    class Meta:
        verbose_name = "кадр из сериала"
        verbose_name_plural = "кадры из сериалов"

    def __str__(self):
        return f"Фото {self.serial.name}"
