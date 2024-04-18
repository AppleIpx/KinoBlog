from factory import Faker
from factory import post_generation
from factory.django import DjangoModelFactory

from some_proj.films.models import FilmModel


class FilmFactory(DjangoModelFactory):
    name = Faker("name")
    trailer = "https://www.youtube.com"
    description = "Описание тестового фильма"
    age_limit = Faker("random_int", min=0, max=21)
    release_date = Faker("date_of_birth")
    duration = Faker("random_int", min=0, max=360)

    @post_generation
    def country(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.country.add(*extracted)

    @post_generation
    def producers(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.producers.add(*extracted)

    @post_generation
    def genre(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.genre.add(*extracted)

    @post_generation
    def actors(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.actors.add(*extracted)

    class Meta:
        model = FilmModel
