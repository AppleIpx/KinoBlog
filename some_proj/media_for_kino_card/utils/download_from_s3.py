from some_proj.media_for_kino_card.tasks import download_file_from_s3


def download(orig_file_path, instance):
    # скачивание файла с S3
    return download_file_from_s3.delay(
        orig_file_path,
        instance.film.name,
        instance.quality,
    )
