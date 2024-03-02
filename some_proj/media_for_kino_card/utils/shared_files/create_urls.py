from some_proj.media_for_kino_card.models import UrlsInMedia


def create_add_links(instance, quality, recording_file_path):
    # создание локальных ссылкок для каждого качества
    url = recording_file_path

    # занесение данных в UrlsInMedia
    UrlsInMedia.objects.create(
        media=instance,
        quality=quality,
        url=url,
    )
