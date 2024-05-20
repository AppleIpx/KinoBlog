from django.contrib.contenttypes.models import ContentType

from some_proj.films.models import FilmModel
from some_proj.films.tests.factories import ReactionFactory


def create_like(film: FilmModel, user, model):
    reaction = ReactionFactory(
        user=user,
        object_id=film.pk,
        content_type=ContentType.objects.get_for_model(model),
        reaction=True,
    )
    reaction.save()
    film.reaction.add(reaction)
