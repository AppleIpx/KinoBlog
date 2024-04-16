from django.contrib.contenttypes.models import ContentType
from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from some_proj.films.models import IsContentWatch
from some_proj.films.tests.factories.media import MediaFactory
from some_proj.users.tests.factories import UserFactory


class WatchFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    object_id = Faker("pyint")
    content_type = SubFactory(ContentType)
    minutes = Faker("pyint")
    media = SubFactory(MediaFactory)

    class Meta:
        model = IsContentWatch
