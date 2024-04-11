from factory import Faker
from factory.django import DjangoModelFactory

from some_proj.films.models import ProducerModel


class ProducerFactory(DjangoModelFactory):
    class Meta:
        model = ProducerModel

    name = Faker("name")
    surname = Faker("name")
    patronymic = Faker("name")
    birthday = Faker("date_of_birth")
    photo = "/Users/Eugeniy/Downloads/Selyanov.jpeg"
