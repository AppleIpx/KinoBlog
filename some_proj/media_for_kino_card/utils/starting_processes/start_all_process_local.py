import logging

from some_proj.media_for_kino_card.models import Quality
from some_proj.media_for_kino_card.utils.celery_files import encoding
from some_proj.media_for_kino_card.utils.celery_files import get_correlation
from some_proj.media_for_kino_card.utils.shared_files import check_instance
from some_proj.media_for_kino_card.utils.shared_files import create_add_links


def start_process_media_files_local(instance):
    orig_file_path = instance.orig_path_file
    qualities = Quality.objects.all()

    # определние объекта: Фильм или Сериал
    content_name = check_instance(instance)

    # Определение соотношения разрешения оригинального фильма
    # получение отношения ширины к высоте исходного кадра
    correlation_value = get_correlation(orig_file_path)
    for quality in qualities:
        # Кодирование видео
        recording_file_path_value = encoding(
            orig_file_path,
            content_name,
            quality,
            correlation_value,
        )
        # Создание и добавление в таблицу локальных ссылок видео-файлов
        create_add_links(
            instance,
            quality,
            recording_file_path_value,
        )
        success_msg_create_link = f"Локальные ссылка для качества {quality.name} успешно создана"
        logging.info(success_msg_create_link)
