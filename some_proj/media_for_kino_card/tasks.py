import boto3
import ffmpeg
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
from celery import shared_task
from django.conf import settings

from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.models import UrlsInMedia
from some_proj.media_for_kino_card.utils.shared_files.check_or_create_local_package import check_or_create_package


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
def get_video_stream(filepath):
    probe = ffmpeg.probe(filepath)
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    width = int(video_stream["width"])
    height = int(video_stream["height"])
    return width / height


@shared_task
def recoding_files(orig_file_path, file_name, quality, correlation):
    output_folder = f"media/{file_name}"
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
def create_add_links_for_amazon(instance, qualities, recording_files_paths):
    # создание ссылки на Amazon для каждого качества
    media_file = MediaFile.objects.create(film=instance.film)
    for quality, file_path in zip(qualities, recording_files_paths, strict=False):
        s3_url = f"https://s3.amazonaws.com/your_bucket_name/{file_path}"
        # занесение данных в UrlsInMedia
        UrlsInMedia.objects.create(
            media=media_file,
            quality=quality,
            url=s3_url,
        )


@shared_task
def create_add_local_links(instance, quality, recording_file_path):
    # создание локальных ссылкок для каждого качества
    local_url = recording_file_path
    # занесение данных в UrlsInMedia
    UrlsInMedia.objects.create(
        media=instance,
        quality=quality,
        url=local_url,
    )


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
