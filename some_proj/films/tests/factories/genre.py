from factory import Faker
from factory.django import DjangoModelFactory

from some_proj.films.models import GenreModel


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = GenreModel

    name = Faker("name")
