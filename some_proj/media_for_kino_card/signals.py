from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from some_proj.films.models import FilmModel
from some_proj.films.models import SerialModel
from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.utils.media_check import media_check_in_s3
from some_proj.media_for_kino_card.utils.start_all_process import start_process_media_files

# Логика такая, что вначале создает карточка фильма
# или сериала, перехватывается сигналом, создается Медия
# со ссылкой на модель, которая только, что была
# создана => медия знает про связь фильма/сериала. После
# обновления Медии (ссылкой на S3) можно запускать процесс
# скачивания файла, кодировки и тп. Это нужно было для
# получения данных о фильме или сериале


@receiver(post_save, sender=FilmModel)
@receiver(post_save, sender=SerialModel)
def create_or_update_media_file(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)
    if created:
        MediaFile.objects.create(content_type=content_type, object_id=instance.id)


@receiver(pre_save, sender=MediaFile)
def update_media_file(sender, instance, created, **kwargs):
    if not created:
        previous_version = MediaFile.history.filter(pk=instance.pk).prev_record
        # проверка на перекодировку
        if media_check_in_s3(previous_version, instance):
            # запуск всех процессов
            start_process_media_files(previous_version)
        MediaFile.objects.filter(pk=instance.pk).update(orig_file=instance.orig_file)
