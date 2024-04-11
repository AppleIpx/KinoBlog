from factory import Faker
from factory.django import DjangoModelFactory

from some_proj.films.models import CountryModel


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = CountryModel

    name = Faker("name")
