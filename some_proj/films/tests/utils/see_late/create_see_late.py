from django.contrib.contenttypes.models import ContentType

from some_proj.films.tests.factories.see_late import SeeLateFactory


def create_see_late(user, film_id, model):
    see_late = SeeLateFactory(
        user=user,
        object_id=film_id,
        content_type=ContentType.objects.get_for_model(model),
    )
    see_late.save()
