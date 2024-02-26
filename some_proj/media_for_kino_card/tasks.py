from pathlib import Path

import boto3
import ffmpeg
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
from celery import shared_task
from django.conf import settings


def ensure_directory_exists(directory_path):
    if not Path.exists(directory_path):
        Path.mkdir(directory_path)


@shared_task
def download_file_from_s3(file_url, file_name, quality=None):
    logger = settings.logging.getLogger("some_proj")
    s3 = boto3.client(
        "s3",
        region_name="eu-central-1",
    )
    bucket_name = "my-bucket"
    file_name_to_save = f"media/{file_name}/{quality}" if quality else f"media/{file_name}"
    try:
        s3.download_file(bucket_name, file_url, file_name_to_save)
        logger.info(
            "Файл %s был успешно скачан и сохранен в %s.",
            file_url,
            file_name_to_save,
        )
    except ClientError:
        logger.exception("Ошибка при скачивании файла:")
    else:
        return file_name_to_save


@shared_task
def recoding_files(orig_file_path, file_name, quality):
    input_file = orig_file_path
    output_folder = file_name
    # проверка на существующую папку
    ensure_directory_exists(output_folder)

    quality_params = {
        "360": {"resolution": "640x360", "video_bitrate": "1000k", "audio_bitrate": "128k"},
        "480": {"resolution": "854x480", "video_bitrate": "1800k", "audio_bitrate": "162k"},
        "720": {"resolution": "1280x720", "video_bitrate": "3500k", "audio_bitrate": "220k"},
        "1080": {"resolution": "1920x1080", "video_bitrate": "8000k", "audio_bitrate": "256k"},
    }
    quality_params = quality_params.get(quality)
    if not quality_params:
        error_message = "Некорректное значение параметра 'quality'"
        raise ValueError(error_message)
    resolution = quality_params["resolution"].split("x")
    vf_filter = f"scale={resolution[0]}:{resolution[1]}"
    output_file = f"{output_folder}/{quality}.mp4"
    command = (
        ffmpeg.input(input_file)
        .output(
            output_file,
            vf=vf_filter,
            **{"b:v": quality_params["video_bitrate"], "b:a": quality_params["audio_bitrate"]},
        )
        .overwrite_output()
    )
    command.run()
    return output_file


@shared_task
def upload_to_s3(file_path, file_name):
    s3 = boto3.client("s3")
    logger = settings.logging.getLogger("some_proj")
    bucket_name = "my-bucket"
    try:
        s3.upload_file(file_path, bucket_name, file_name)
    except FileNotFoundError:
        logger.info("Файл не найден: %s", file_path)
        return False
    except NoCredentialsError:
        logger.info("AWS credentials не найдены.")
        return False
    else:
        logger.info("Файл успешно загружен на S3")
        return True
