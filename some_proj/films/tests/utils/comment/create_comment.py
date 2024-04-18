from django.contrib.contenttypes.models import ContentType
from rest_framework.status import HTTP_401_UNAUTHORIZED

from some_proj.films.tests.factories.comment import CommentFactory


def create_comment(content_id, model, user=None):
    if user:
        comment = CommentFactory(
            user=user,
            object_id=content_id,
            content_type=ContentType.objects.get_for_model(model),
        )
        comment.save()
    return HTTP_401_UNAUTHORIZED
