import logging

from django.conf import settings


def check_env_files():
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    aws_storage_bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    if aws_access_key_id is not None and aws_secret_access_key is not None and aws_storage_bucket_name is not None:
        env_message = "Переменные для подключения к S3 обнаружены"
        logging.info(env_message)
        return True
    warning_message = "Необходимо установить переменные окружения для подключения к S3."
    logging.warning(warning_message)
    return False
