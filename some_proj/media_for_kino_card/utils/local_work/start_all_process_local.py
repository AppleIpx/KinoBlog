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
    correlation = get_video_stream(
        orig_file_path,
    )
    logging.info("Соотношение определено")
    for quality in qualities:
        # Кодирование видео
        recording_file_path = recoding_files(
            orig_file_path,
            film.name,
            quality.name,
            correlation,
        )
        logging.info("Кодирование прошло успешно")
        # Создание и добавление в таблицу локальных ссылок видео-файлов
        create_add_local_links(
            instance,
            quality,
            recording_file_path,
        )
        logging.info("Локальные ссылки успешно созданы")
