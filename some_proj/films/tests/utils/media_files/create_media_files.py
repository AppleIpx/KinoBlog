from django.contrib.contenttypes.models import ContentType

from some_proj.media_for_kino_card.models import MediaFile


def create_media(model, model_id):
    return MediaFile.objects.create(
        content_type=ContentType.objects.get_for_model(model),
        object_id=model_id,
    )
