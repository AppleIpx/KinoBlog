from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from some_proj.films.models import FilmModel
from some_proj.films.models import SerialModel
from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.models import Quality
from some_proj.media_for_kino_card.models import UrlsAmazonInMedia
from some_proj.media_for_kino_card.tasks import download_file_from_s3
from some_proj.media_for_kino_card.tasks import recoding_files
from some_proj.media_for_kino_card.tasks import upload_to_s3


def download(orig_file_path, instance):
    # скачивание файла с S3
    return download_file_from_s3.delay(
        orig_file_path,
        instance.film.name,
        instance.quality,
    )


def recoding(instance, orig_local_path, qualities):
    # Перекодирование исходного файла в 4 качества
    return [
        recoding_files.delay(
            orig_local_path,
            instance.film.name,
            quality.name,
        )
        for quality in qualities
    ]


def create_add_links_for_amazon(instance, qualities, recording_files_paths):
    # создание ссылки на Amazon для каждого качества
    media_file = MediaFile.objects.create(film=instance.film)
    for quality, file_path in zip(qualities, recording_files_paths, strict=False):
        s3_url = f"https://s3.amazonaws.com/your_bucket_name/{file_path}"
        # занесение данных в UrlsAmazonInMedia
        UrlsAmazonInMedia.objects.create(
            media=media_file,
            quality=quality,
            url=s3_url,
        )


def upload(recording_files_paths, file_name):
    # имя файла
    return upload_to_s3.delay(recording_files_paths, file_name)


# запуск всех процессов
def start_process_media_files(instance):
    orig_file_path = instance.orig_file
    qualities = Quality.object.all()

    # Скачивание файла с S3
    orig_local_path = download(
        orig_file_path,
        instance,
    )
    # Кодирование видео
    recording_files_paths = recoding(
        instance,
        orig_local_path,
        qualities,
    )
    # Создание и добавление в таблицу ссылок видео-файлов на S3
    create_add_links_for_amazon(
        instance,
        qualities,
        recording_files_paths,
    )
    # загрузка перекодированных фильмов на S3
    upload(
        recording_files_paths,
        f"{instance.film.name}/{instance.quality}",
    )


# Проверяется изменилась ли ссылка на исходное видео
def media_check_in_s3(previous_version, instance):
    return previous_version.url != instance.urls and previous_version


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
