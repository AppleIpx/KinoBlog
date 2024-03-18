from django.conf import settings


def check_env_files():
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    aws_storage_bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    return aws_access_key_id is not None and aws_secret_access_key is not None and aws_storage_bucket_name is not None
