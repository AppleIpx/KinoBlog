import pytest

from some_proj.films.models import FilmModel
from some_proj.films.tests.utils import TestBaseFilm
from some_proj.films.tests.utils import create_dislike
from some_proj.films.tests.utils import create_like


@pytest.mark.django_db()
class TestReactionsFilms(TestBaseFilm):
    def test_check_default_reaction(self):
        count_likes = self.test_film.reaction.filter(reaction=True).count()
        count_dislikes = self.test_film.reaction.filter(reaction=False).count()
        self.assertEqual(count_likes, 0, count_likes)
        self.assertEqual(count_dislikes, 0, count_dislikes)

    def test_check_admin_like(self):
        create_like(self.test_film, self.test_admin, FilmModel)
        count_likes = self.test_film.reaction.filter(reaction=True).count()
        self.assertEqual(count_likes, 1, count_likes)

    def test_check_admin_dislike(self):
        create_dislike(self.test_film, self.test_auth_user, FilmModel)
        count_dislikes = self.test_film.reaction.filter(reaction=False).count()
        self.assertEqual(count_dislikes, 1, count_dislikes)

    def test_check_auth_user_like(self):
        create_like(self.test_film, self.test_auth_user, FilmModel)
        count_likes = self.test_film.reaction.filter(reaction=True).count()
        self.assertEqual(count_likes, 1, count_likes)

    def test_check_auth_user_dislike(self):
        create_dislike(self.test_film, self.test_auth_user, FilmModel)
        count_dislikes = self.test_film.reaction.filter(reaction=False).count()
        self.assertEqual(count_dislikes, 1, count_dislikes)
