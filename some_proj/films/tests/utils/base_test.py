from rest_framework.test import APITestCase

from some_proj.films.tests.factories import ActorFactory
from some_proj.films.tests.factories import CountryFactory
from some_proj.films.tests.factories import FilmFactory
from some_proj.films.tests.factories import GenreFactory
from some_proj.films.tests.factories import ProducerFactory
from some_proj.users.tests.factories import UserFactory


class TestBaseFilm(APITestCase):
    base_fields = [
        "id",
        "poster",
        "posters",
        "name",
        "release_date",
        "duration",
        "age_limit",
        "poster",
        "posters",
    ]
    list_fields = [
        "is_favorite",
        "like_count",
        "dislike_count",
    ]
    retrieve_fields = [
        "urls",
        "is_watched",
        "is_see_late",
        "description",
        "trailer",
        "producers",
        "cadrs",
        "actors",
        "country",
        "genre",
        "comments",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        country = CountryFactory()
        genre = GenreFactory()
        actors = ActorFactory()
        producers = ProducerFactory()
        cls.test_film = FilmFactory.create(
            country=[country],
            genre=[genre],
            actors=[actors],
            producers=[producers],
        )
        cls.test_admin = UserFactory(is_staff=True)
        cls.test_auth_user = UserFactory(is_staff=False)
