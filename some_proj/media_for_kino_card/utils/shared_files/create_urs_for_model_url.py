from django.conf import settings


def create_links(content_name, quality):
    return f"{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}/videos/{content_name}/{quality}.mp4"
