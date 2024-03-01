import logging

from some_proj.films.models import FilmModel
from some_proj.media_for_kino_card.models import Quality
from some_proj.media_for_kino_card.tasks import create_add_local_links
from some_proj.media_for_kino_card.tasks import get_video_stream
from some_proj.media_for_kino_card.tasks import recoding_files


def start_process_media_files_local(instance):
    orig_file_path = instance.orig_path_file
    qualities = Quality.objects.all()
    film = FilmModel.objects.get(pk=instance.object_id)

    # Определение соотношения разрешения оригинального фильма
    correlation = get_video_stream.delay(
        orig_file_path,
    )
    correlation_value = correlation.get(timeout=10)
    logging.info("Соотношение определено")
    for quality in qualities:
        # Кодирование видео
        recording_file_path = recoding_files.delay(
            orig_file_path,
            film.name,
            quality.name,
            correlation_value,
        )
        recording_file_value = recording_file_path.get(propagate=False)
        success_msg_recording = f"Кодирование качества{quality.name} прошло успешно"
        logging.info(success_msg_recording)

        # Создание и добавление в таблицу локальных ссылок видео-файлов
        instance_id = instance.object_id
        quality_id = quality.pk
        create_add_local_links.delay(
            instance_id,
            quality_id,
            recording_file_value,
        )
        success_msg_create_link = f"Локальные ссылка для качества {quality.name} успешно создана"
        logging.info(success_msg_create_link)
