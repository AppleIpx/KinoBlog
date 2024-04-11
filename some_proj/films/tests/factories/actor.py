from factory import Faker
from factory.django import DjangoModelFactory

from some_proj.films.models import ActorModel


class ActorFactory(DjangoModelFactory):
    class Meta:
        model = ActorModel

    name = Faker("name")
    surname = Faker("name")
    patronymic = Faker("name")
    birthday = Faker("date_of_birth")
    photo = "/Users/Eugeniy/Downloads/bortich.jpeg"
