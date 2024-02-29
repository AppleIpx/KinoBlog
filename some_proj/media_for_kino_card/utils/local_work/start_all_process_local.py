import logging

from some_proj.films.models import FilmModel
from some_proj.media_for_kino_card.models import Quality
from some_proj.media_for_kino_card.tasks import create_add_local_links
from some_proj.media_for_kino_card.utils.work_with_s3.defining_the_resolution import start_process_get_correlation
from some_proj.media_for_kino_card.utils.work_with_s3.recoding_files import recoding


def start_process_media_files_local(instance):
    orig_file_path = instance.orig_path_file
    qualities = Quality.objects.all()
    film = FilmModel.objects.get(pk=instance.object_id)
    # Определение соотношения разрешения оригинального фильма
    correlation = start_process_get_correlation(
        orig_file_path,
    )
    logging.info("Соотношение определено")
    # Кодирование видео
    recording_files_paths = recoding(
        film.name,
        orig_file_path,
        qualities,
        correlation,
    )
    logging.info("Кодирование прошло успешно")
    # Создание и добавление в таблицу локальных ссылок видео-файлов
    create_add_local_links(
        instance,
        qualities,
        recording_files_paths,
    )
    logging.info("Локальные ссылки успешно созданы")
