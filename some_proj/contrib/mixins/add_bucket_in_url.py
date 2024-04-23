from django.conf import settings


class AddBucketMixin:
    def add_bucket_name(self, url, item):
        bucket_name = f"{settings.AWS_STORAGE_BUCKET_NAME}/"
        return url.replace(f"{item}", f"{bucket_name}{item}", 1)
