from django.contrib.contenttypes.models import ContentType

from some_proj.films.models import FavoriteContent


def delete_favorite(user, film_id, model):
    FavoriteContent.objects.filter(
        user=user,
        object_id=film_id,
        content_type=ContentType.objects.get_for_model(model),
    ).delete()
