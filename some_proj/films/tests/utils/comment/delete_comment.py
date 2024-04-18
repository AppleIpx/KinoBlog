from django.contrib.contenttypes.models import ContentType
from rest_framework.status import HTTP_401_UNAUTHORIZED

from some_proj.comments.models import CommentModel


def delete_comments(content_id, model, user=None):
    if user:
        CommentModel.objects.filter(
            user=user,
            object_id=content_id,
            content_type=ContentType.objects.get_for_model(model),
        ).delete()
    return HTTP_401_UNAUTHORIZED
