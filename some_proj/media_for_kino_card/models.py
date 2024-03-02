from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from simple_history.models import HistoricalRecords


class Quality(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = "Качество"
        verbose_name_plural = "Качества"

    def __str__(self):
        return self.name


class MediaFile(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    content_object = GenericForeignKey("content_type", "object_id")
    episode = models.CharField(
        verbose_name="Выбор эпизода фильма",
        max_length=255,
    )
    orig_path_file = models.CharField(
        max_length=300,
        verbose_name="Ссылка на исходный локальный файл / S3",
    )
    data_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
    )
    urls = models.ManyToManyField(
        "UrlsInMedia",
        verbose_name="Ссылки на видеофайлы",
        related_name="media_urls",
        blank=True,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Медия"
        verbose_name_plural = "Медии"

    def __str__(self):
        return (
            f"{self.content_object.name} {self.content_object.season} сезон {self.episode} серия"
            if hasattr(self.content_object, "season")
            else self.content_object.name
        )


class UrlsInMedia(models.Model):
    media = models.ForeignKey(
        MediaFile,
        verbose_name="Медиа",
        on_delete=models.CASCADE,
    )
    quality = models.ForeignKey(
        Quality,
        verbose_name="качество",
        on_delete=models.CASCADE,
    )
    url = models.CharField(
        verbose_name="ссылка",
        max_length=300,
        default="",
    )

    class Meta:
        verbose_name = "Ссылка на амазон"
        verbose_name_plural = "Ссылки на амазон"

    def __str__(self):
        return f"{self.media} - {self.quality}"
