from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.models import UrlsAmazonInMedia


def create_add_links_for_amazon(instance, qualities, recording_files_paths):
    # создание ссылки на Amazon для каждого качества
    media_file = MediaFile.objects.create(film=instance.film)
    for quality, file_path in zip(qualities, recording_files_paths, strict=False):
        s3_url = f"https://s3.amazonaws.com/your_bucket_name/{file_path}"
        # занесение данных в UrlsAmazonInMedia
        UrlsAmazonInMedia.objects.create(
            media=media_file,
            quality=quality,
            url=s3_url,
        )
