from django.contrib.contenttypes.models import ContentType
from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from some_proj.comments.models import CommentModel
from some_proj.users.tests.factories import UserFactory


class CommentFactory(DjangoModelFactory):
    text = Faker("text")
    user = SubFactory(UserFactory)
    object_id = Faker("pyint")
    content_type = SubFactory(ContentType)
    created_at = Faker("date")

    class Meta:
        model = CommentModel
