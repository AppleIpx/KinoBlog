from factory import Faker
from factory.django import DjangoModelFactory

from some_proj.films.models import CountryModel


class CountryFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = CountryModel
