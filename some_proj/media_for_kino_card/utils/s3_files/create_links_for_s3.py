import pathlib
from uuid import uuid4

from django.conf import settings


def create_links(quality, file_name):
    # хэширование имени файла и качества
    hash_file_name = pathlib.Path(file_name).suffix
    hash_quality = pathlib.Path(quality.name).suffix
    hash_file_name, hash_quality = f"{uuid4().hex}{hash_file_name}", f"{uuid4().hex}{hash_quality}"

    # создание ссылки в стиле s3 для отображения в Api
    url_api_s3 = (
        f"{settings.AWS_S3_ENDPOINT_URL}/"
        f"{settings.AWS_STORAGE_BUCKET_NAME}/"
        f"videos/{hash_file_name}/{hash_quality}.mp4"
    )

    # генерирование ссылки для загрузки файла в с3
    s3_url = f"videos/{hash_file_name}/{hash_quality}.mp4"
    return url_api_s3, s3_url
