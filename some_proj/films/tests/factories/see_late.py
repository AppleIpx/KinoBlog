from django.contrib.contenttypes.models import ContentType
from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from some_proj.films.models import SeeLateContent
from some_proj.users.tests.factories import UserFactory


class SeeLateFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    object_id = Faker("pyint")
    content_type = SubFactory(ContentType)

    class Meta:
        model = SeeLateContent
