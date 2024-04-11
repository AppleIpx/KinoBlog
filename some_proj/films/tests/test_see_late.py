import pytest
from django.urls import reverse

from some_proj.films.models import FilmModel
from some_proj.films.tests.utils import TestBaseFilm
from some_proj.films.tests.utils import check_status
from some_proj.films.tests.utils.see_late.create_see_late import create_see_late
from some_proj.films.tests.utils.watch.delete_watch import delete_watch


@pytest.mark.django_db()
class TestSeeLateFilms(TestBaseFilm):
    def _check_see_late_status(self, user, expected_value):
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse(
                "api:films-detail",
                kwargs={"pk": self.test_film.id},
            ),
        )
        check_status(response)
        self.assertEqual(
            response.data["is_see_late"],
            expected_value,
            f"Должно было быть {expected_value}",
        )

    def test_check_default_admin_see_late(self):
        self._check_see_late_status(
            user=self.test_admin,
            expected_value=False,
        )

    def test_check_add_admin_see_late(self):
        create_see_late(
            self.test_admin,
            self.test_film.id,
            FilmModel,
        )
        self._check_see_late_status(
            user=self.test_admin,
            expected_value=True,
        )

    def test_check_delete_admin_see_late(self):
        delete_watch(
            self.test_admin,
            self.test_film.id,
            FilmModel,
        )
        self._check_see_late_status(
            user=self.test_admin,
            expected_value=False,
        )

    def test_check_default_auth_user_see_late(self):
        self._check_see_late_status(
            user=self.test_auth_user,
            expected_value=False,
        )

    def test_check_add_auth_user_see_late(self):
        create_see_late(
            self.test_auth_user,
            self.test_film.id,
            FilmModel,
        )
        self._check_see_late_status(
            user=self.test_auth_user,
            expected_value=True,
        )

    def test_check_delete_auth_user_see_late(self):
        delete_watch(
            self.test_auth_user,
            self.test_film.id,
            FilmModel,
        )
        self._check_see_late_status(
            user=self.test_auth_user,
            expected_value=False,
        )
