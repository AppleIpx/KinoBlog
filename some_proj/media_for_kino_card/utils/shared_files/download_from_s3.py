import logging

from some_proj.media_for_kino_card.tasks import download_file_from_s3


def download_file_s3(s3_path_to_file, content_name):
    download_start_message = "Начало загрузки исходного файла с s3"
    logging.info(download_start_message)

    # Скачивание файла с S3
    orig_local_path = download_file_from_s3.delay(
        s3_path_to_file,
        content_name,
    )
    orig_local_path_value = orig_local_path.get(timeout=400)

    download_message = "Оригинальный файл успешно скачан"
    logging.info(download_message)
    return orig_local_path_value
