from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from some_proj.films.models import FilmModel
from some_proj.films.models import SerialModel
from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.utils.executing_processes_in_signal import start_signal_processes

# Логика такая, что вначале создает карточка фильма
# или сериала, перехватывается сигналом, создается Медия
# со ссылкой на модель, которая только, что была
# создана => медия знает про связь фильма/сериала. После
# обновления Медии (ссылкой на S3) можно запускать процесс
# скачивания файла, кодировки и тп. Это нужно было для
# получения данных о фильме или сериале


@receiver(post_save, sender=SerialModel)
@receiver(post_save, sender=FilmModel)
def create_media_file(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)
    if created:
        MediaFile.objects.create(content_type=content_type, object_id=instance.id)


@receiver(pre_save, sender=MediaFile)
def update_media_file(sender, instance, **kwargs):
    if instance.pk:
        start_signal_processes(instance)
