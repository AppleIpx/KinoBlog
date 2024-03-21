import ffmpeg
from celery import shared_task

from some_proj.media_for_kino_card.S3.s3_client import s3_current_client
from some_proj.media_for_kino_card.utils.shared_files import check_or_create_package
from some_proj.media_for_kino_card.utils.shared_files import extract_name


@shared_task
def download_file_from_s3(s3_path_to_file, content_name):
    output_folder = f"some_proj/media/media_s3/orig_videos/{content_name}/"
    # создание локальной папки
    check_or_create_package(output_folder)

    # извлекаем имя файла из url и генерируем локальные ссылки
    filename, output_folder = extract_name(output_folder, s3_path_to_file)

    return s3_current_client.download_content(filename, output_folder)


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
def upload_to_s3(local_path, s3_url):
    return s3_current_client.upload_content(local_path, s3_url)
