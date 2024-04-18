import pytest
from django.urls import reverse

from some_proj.films.models import FilmModel
from some_proj.films.tests.utils import TestBaseFilm
from some_proj.films.tests.utils import check_status
from some_proj.films.tests.utils.favorite.create_favorite import create_favorite
from some_proj.films.tests.utils.favorite.delete_favorite import delete_favorite


@pytest.mark.django_db()
class TestFavoriteFilms(TestBaseFilm):
    def _check_favorite_status(self, user, expected_value):
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse(
                "api:films-detail",
                kwargs={"pk": self.test_film.id},
            ),
        )
        check_status(response)
        self.assertEqual(
            response.data["is_favorite"],
            expected_value,
            f"Должно было быть {expected_value}",
        )

    def test_check_default_admin_favorite(self):
        self._check_favorite_status(
            user=self.test_admin,
            expected_value=False,
        )

    def test_check_add_admin_favorite(self):
        create_favorite(
            self.test_admin,
            self.test_film.id,
            FilmModel,
        )
        self._check_favorite_status(
            user=self.test_admin,
            expected_value=True,
        )

    def test_check_delete_admin_favorite(self):
        delete_favorite(
            user=self.test_admin,
            film_id=self.test_film.id,
            model=FilmModel,
        )
        self._check_favorite_status(
            user=self.test_admin,
            expected_value=False,
        )

    def test_check_default_auth_user_favorite(self):
        self._check_favorite_status(
            user=self.test_auth_user,
            expected_value=False,
        )

    def test_check_add_auth_user_favorite(self):
        create_favorite(
            self.test_auth_user,
            self.test_film.id,
            FilmModel,
        )
        self._check_favorite_status(
            user=self.test_auth_user,
            expected_value=True,
        )

    def test_check_delete_auth_user_favorite(self):
        delete_favorite(
            self.test_auth_user,
            self.test_film.id,
            FilmModel,
        )
        self._check_favorite_status(
            user=self.test_auth_user,
            expected_value=False,
        )
