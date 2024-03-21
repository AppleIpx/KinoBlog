import logging

from some_proj.media_for_kino_card.models import Quality
from some_proj.media_for_kino_card.tasks import upload_to_s3
from some_proj.media_for_kino_card.utils.shared_files import check_instance
from some_proj.media_for_kino_card.utils.shared_files import create_add_links
from some_proj.media_for_kino_card.utils.shared_files import create_links
from some_proj.media_for_kino_card.utils.shared_files import download_file_s3
from some_proj.media_for_kino_card.utils.shared_files import encoding
from some_proj.media_for_kino_card.utils.shared_files import get_correlation


# запуск всех процессов s3
def start_process_media_files_s3(instance):
    s3_path_to_file = instance.orig_path_file
    qualities = Quality.objects.all()

    # определение объекта: Фильм или Сериал
    content_name, file_name = check_instance(instance)

    # скачивание файла с s3
    orig_local_path_value = download_file_s3(
        s3_path_to_file,
        content_name,
    )
    # получение отношения ширины к высоте исходного кадра
    correlation_value = get_correlation(orig_local_path_value)

    for quality in qualities:
        recording_file_path_value = encoding(
            orig_local_path_value,
            content_name,
            quality,
            correlation_value,
        )
        # создание ссылки для отображения в api
        # создание ссылки для загрузки файла внутри с3
        s3_url_for_api, s3_url = create_links(quality, file_name)

        # Создание и добавление в таблицу ссылок видео-файлов на S3
        create_add_links(
            instance,
            quality,
            s3_url_for_api,
        )
        # загрузка перекодированных фильмов на S3
        uploading_message = f"Файл {instance.content_object.name} {quality.name} загружается на s3"
        logging.info(uploading_message)

        answer = upload_to_s3.delay(recording_file_path_value, s3_url)

        if answer.get(propagate=False):
            answer_message = "Файл успешно загружен"
            logging.info(answer_message)
