from django.contrib.auth import get_user_model
from django.db import models

from some_proj.films.models import BaseContentModel

User = get_user_model()


class SerialModel(BaseContentModel):
    season = models.PositiveIntegerField(
        verbose_name="Сезон",
    )
    num_serials = models.PositiveIntegerField(
        verbose_name="Кол-во серий",
    )
    release_date = models.DateField(
        verbose_name="Дата выхода сериала",
    )
    duration = models.IntegerField(
        verbose_name="длительность серии",
    )

    class Meta:
        verbose_name = "сериал"
        verbose_name_plural = "сериалы"

    def __str__(self):
        return f"{self.name} {self.season} сезон"


class PhotoSerial(models.Model):
    serial = models.ForeignKey(
        SerialModel,
        verbose_name="сериал",
        on_delete=models.CASCADE,
    )
    photo_serial = models.ImageField(
        upload_to=f"media/photos_serials/{serial.name}",
        verbose_name="Кадр из сериала",
    )

    class Meta:
        verbose_name = "Фотография из сериала"
        verbose_name_plural = "Фотографии из сериалов"

    def __str__(self):
        return f"Фото {self.serial.name}"
