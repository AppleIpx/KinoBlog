import logging

from some_proj.media_for_kino_card.models import Quality
from some_proj.media_for_kino_card.tasks import download_file_from_s3
from some_proj.media_for_kino_card.tasks import get_video_stream
from some_proj.media_for_kino_card.tasks import recoding_files
from some_proj.media_for_kino_card.tasks import upload_to_s3
from some_proj.media_for_kino_card.utils.shared_files import check_instance
from some_proj.media_for_kino_card.utils.shared_files import create_add_links


# запуск всех процессов
def start_process_media_files_s3(instance):
    s3_path_to_file = instance.orig_path_file
    qualities = Quality.objects.all()

    # определение объекта: Фильм или Сериал
    content_name = check_instance(instance)
    object_message = "Объект определен"
    logging.info(object_message)

    # Скачивание файла с S3
    orig_local_path = download_file_from_s3.delay(
        s3_path_to_file,
        content_name,
    )
    download_message = "Оригинальный файл успешно скачан"
    logging.info(download_message)
    orig_local_path_value = orig_local_path.get(timeout=30)

    # Определение соотношения разрешения оригинального фильма
    correlation = get_video_stream.delay(
        orig_local_path_value,
    )
    correlation_message = "Соотношение определено"
    logging.info(correlation_message)
    correlation_value = correlation.get(timeout=10)
    for quality in qualities:
        # Кодирование видео
        recording_file_path = recoding_files.delay(
            orig_local_path,
            content_name,
            quality.name,
            correlation_value,
        )
        success_msg_recording = f"Кодирование качества{quality.name} прошло успешно"
        logging.info(success_msg_recording)
        recording_file_value = recording_file_path.get(propagate=False)

        # Создание и добавление в таблицу ссылок видео-файлов на S3
        create_add_links(
            instance,
            quality,
            recording_file_value,
        )
        success_msg_create_link = f"Ссылка для качества {quality.name} успешно создана"
        logging.info(success_msg_create_link)

        # загрузка перекодированных фильмов на S3
        upload_to_s3.delay(recording_file_value)
        upload_message = f"Файл {instance.content_object.name} {quality.name} успешно загружен на s3"
        logging.info(upload_message)
