from django.contrib.contenttypes.models import ContentType
from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from some_proj.media_for_kino_card.models import MediaFile
from some_proj.users.tests.factories import UserFactory


class MediaFactory(DjangoModelFactory):
    class Meta:
        model = MediaFile

    user = SubFactory(UserFactory)
    object_id = Faker("pyint")
    content_type = SubFactory(ContentType)
    minutes = Faker("pyint")
    data_added = Faker("date_of_birth")
    episode = Faker("pyint")
    orig_path_file = Faker("url")
