from django.conf import settings

from some_proj.media_for_kino_card.S3.s3 import S3

s3_current_client = S3(settings.AWS_STORAGE_BUCKET_NAME)
