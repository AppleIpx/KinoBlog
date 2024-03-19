import logging
from urllib.parse import urlparse

import ffmpeg
from botocore.exceptions import ClientError
from celery import shared_task
from django.conf import settings

from some_proj.media_for_kino_card.utils.connect_to_s3 import connect_s3
from some_proj.media_for_kino_card.utils.shared_files.check_or_create_local_package import check_or_create_package


@shared_task
def download_file_from_s3(s3_path_to_file, content_name):
    output_folder = f"some_proj/media/media_s3/orig_videos/{content_name}/"
    # создание папки
    check_or_create_package(output_folder)

    # извлекаем имя файла из url
    parts = output_folder.split("/")
    output_folder = output_folder + f"{parts[-2]}.mp4"

    # создание подключения к s3
    s3 = connect_s3()

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    parsed_url = urlparse(s3_path_to_file).path
    filename = parsed_url[parsed_url.index("orig_videos") :]
    try:
        s3.download_file(bucket_name, filename, output_folder)
        download_message = f"Файл {content_name} был успешно скачан и сохранен в {output_folder}."
        logging.info(download_message)
    except ClientError:
        exception_message = "Ошибка при скачивании файла"
        logging.exception(exception_message)
    else:
        success_message = "Скачивание файла прошло успешно"
        logging.info(success_message)
        return output_folder


@shared_task
def get_video_stream(filepath):
    probe = ffmpeg.probe(filepath)
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    width = int(video_stream["width"])
    height = int(video_stream["height"])
    return width / height


@shared_task
def recoding_files(orig_file_path, content_name, quality, correlation):
    output_folder = f"some_proj/media/videos/{content_name}"
    # проверка на существующую папку
    check_or_create_package(output_folder)
    quality_params = {
        "360": {
            "video_bitrate": "1000k",
            "audio_bitrate": "128k",
        },
        "480": {
            "video_bitrate": "1800k",
            "audio_bitrate": "162k",
        },
        "720": {
            "video_bitrate": "3500k",
            "audio_bitrate": "220k",
        },
        "1080": {
            "video_bitrate": "8000k",
            "audio_bitrate": "256k",
        },
    }
    width = round(int(quality) * correlation)
    height = int(quality)
    # проверка на четность и нечетность ширины
    if width % 2 != 0:
        width += 1
    vf_filter = f"scale={width}:{height}, fps=23.976"
    output_file = f"{output_folder}/{quality}.mp4"
    command = (
        ffmpeg.input(orig_file_path)
        .output(
            output_file,
            vf=vf_filter,
            **{
                "b:v": quality_params[quality]["video_bitrate"],
                "b:a": quality_params[quality]["audio_bitrate"],
            },
        )
        .overwrite_output()
    )
    command.run()
    return output_file


@shared_task
def upload_to_s3(recording_file_value, s3_url):
    # подключение к s3
    s3 = connect_s3()
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    local_path = recording_file_value
    path_s3 = s3_url
    try:
        s3.upload_file(local_path, bucket_name, path_s3)
    except FileNotFoundError:
        message_file_not_found = f"Файл {recording_file_value}не найден"
        logging.info(message_file_not_found)
        return message_file_not_found
    else:
        success_message = "Файл успешно загружен на S3"
        logging.info(success_message)
        return success_message
