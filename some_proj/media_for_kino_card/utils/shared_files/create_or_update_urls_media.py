import logging

from some_proj.media_for_kino_card.models import UrlsInMedia


def create_add_links(instance, quality, recording_file_path):
    url = recording_file_path
    url_media, created = UrlsInMedia.objects.get_or_create(
        media=instance,
        quality=quality,
        defaults={"url": url},
    )

    if not created:
        # Объект уже существует, обновляем его данные
        url_media.url = url
        url_media.save()

    success_msg_create_link = f"Ссылка для качества {quality.name} успешно создана"
    logging.info(success_msg_create_link)
