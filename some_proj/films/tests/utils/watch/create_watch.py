from django.contrib.contenttypes.models import ContentType

from some_proj.films.tests.factories.watch import WatchFactory
from some_proj.media_for_kino_card.models import MediaFile


def create_watch(user, film_id, model):
    content_type = ContentType.objects.get_for_model(model)
    media = MediaFile.objects.filter(
        object_id=film_id,
        content_type=content_type,
    ).first()
    watch = WatchFactory(
        user=user,
        object_id=film_id,
        content_type=content_type,
        media=media,
    )
    watch.save()
