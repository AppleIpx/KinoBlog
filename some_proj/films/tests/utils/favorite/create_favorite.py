from django.contrib.contenttypes.models import ContentType

from some_proj.films.tests.factories.favorite import FavoriteFactory


def create_favorite(user, film_id, model):
    favorite = FavoriteFactory(
        user=user,
        object_id=film_id,
        content_type=ContentType.objects.get_for_model(model),
    )
    favorite.save()
