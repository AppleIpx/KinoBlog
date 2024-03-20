import logging

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from django.conf import settings


class S3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
            region_name=settings.AWS_S3_REGION_NAME,
        )

    def download_content(self, file_name, output_folder):
        try:
            self.client.download_file(self.bucket_name, file_name, output_folder)
            download_message = f"Файл {file_name} был успешно скачан и сохранен в {output_folder}."
            logging.info(download_message)
        except ClientError:
            exception_message = "Ошибка при скачивании файла"
            logging.exception(exception_message)
        else:
            success_message = "Скачивание файла прошло успешно"
            logging.info(success_message)
            return output_folder

    def upload_content(self, local_path, path_s3):
        try:
            self.client.upload_file(local_path, self.bucket_name, path_s3)
        except FileNotFoundError:
            message_file_not_found = f"Файл {local_path}не найден"
            logging.info(message_file_not_found)
            return message_file_not_found
        else:
            success_message = "Файл успешно загружен на S3"
            logging.info(success_message)
            return success_message
