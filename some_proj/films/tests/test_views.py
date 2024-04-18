import pytest
from django.urls import reverse

from some_proj.films.tests.utils import check_admin_list_fields
from some_proj.films.tests.utils import check_admin_not_list_fields
from some_proj.films.tests.utils import check_admin_retrieve_fields
from some_proj.films.tests.utils import check_anonymous_list_fields
from some_proj.films.tests.utils import check_anonymous_not_list_fields
from some_proj.films.tests.utils import check_anonymous_retrieve_fields
from some_proj.films.tests.utils import check_auth_user_list_fields
from some_proj.films.tests.utils import check_auth_user_not_list_fields
from some_proj.films.tests.utils import check_auth_user_retrieve_fields
from some_proj.films.tests.utils import check_status
from some_proj.films.tests.utils.base_test import TestBaseFilm


@pytest.mark.django_db()
class TestFilmsView(TestBaseFilm):
    def _get_list_response(self, user=None):
        if user:
            self.client.force_authenticate(user=user)
        response = self.client.get(reverse("api:films-list"))
        check_status(response)
        return response

    def _get_retrieve_response(self, test_film_id, user=None):
        if user:
            self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse(
                "api:films-detail",
                kwargs={"pk": test_film_id},
            ),
        )
        check_status(response)
        return response

    def test_admin_list_fields(self):
        response = self._get_list_response(user=self.test_admin)
        check_admin_list_fields(self, response)
        check_admin_not_list_fields(self, response)

    def test_admin_retrieve_fields(self):
        test_film_id = self.test_film.id
        response = self._get_retrieve_response(
            test_film_id,
            user=self.test_admin,
        )
        check_admin_retrieve_fields(self, response)

    def test_auth_user_list_fields(self):
        response = self._get_list_response(user=self.test_auth_user)
        check_auth_user_list_fields(self, response)
        check_auth_user_not_list_fields(self, response)

    def test_auth_user_retrieve_fields(self):
        test_film_id = self.test_film.id
        response = self._get_retrieve_response(
            test_film_id,
            user=self.test_auth_user,
        )
        check_auth_user_retrieve_fields(self, response)

    def test_anonymous_list_fields(self):
        response = self._get_list_response()
        check_anonymous_list_fields(self, response)
        check_anonymous_not_list_fields(self, response)

    def test_anonymous_retrieve_fields(self):
        test_film_id = self.test_film.id
        response = self._get_retrieve_response(test_film_id)
        check_anonymous_retrieve_fields(self, response)
