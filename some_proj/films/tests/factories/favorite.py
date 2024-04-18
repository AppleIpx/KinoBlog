from django.contrib.contenttypes.models import ContentType
from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from some_proj.films.models import FavoriteContent
from some_proj.users.tests.factories import UserFactory


class FavoriteFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    object_id = Faker("pyint")
    content_type = SubFactory(ContentType)

    class Meta:
        model = FavoriteContent
