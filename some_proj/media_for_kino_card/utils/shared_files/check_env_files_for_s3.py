from django.conf import settings


def check_env_files():
    django_aws_access_key_id = settings.DJANGO_AWS_ACCESS_KEY_ID
    django_aws_secret_access_key = settings.DJANGO_AWS_SECRET_ACCESS_KEY
    django_aws_storage_bucket_name = settings.DJANGO_AWS_STORAGE_BUCKET_NAME
    return (
        django_aws_access_key_id is not None
        and django_aws_secret_access_key is not None
        and django_aws_storage_bucket_name is not None
    )
