from django.contrib.contenttypes.models import ContentType

from some_proj.films.models import IsContentWatch


def delete_watch(user, film_id, model):
    IsContentWatch.objects.filter(
        user=user,
        object_id=film_id,
        content_type=ContentType.objects.get_for_model(model),
    ).delete()
