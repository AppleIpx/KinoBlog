import boto3
from botocore.config import Config
from django.conf import settings


def connect_s3():
    return boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_CUSTOM_DOMAIN,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
        region_name=settings.AWS_S3_REGION_NAME,
    )
