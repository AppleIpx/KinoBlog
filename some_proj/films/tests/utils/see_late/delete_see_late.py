from django.contrib.contenttypes.models import ContentType

from some_proj.films.models import SeeLateContent


def delete_see_late(user, film_id, model):
    SeeLateContent.objects.filter(
        user=user,
        object_id=film_id,
        content_type=ContentType.objects.get_for_model(model),
    ).delete()
