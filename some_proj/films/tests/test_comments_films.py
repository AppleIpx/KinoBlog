from django.urls import reverse

from some_proj.films.models import FilmModel
from some_proj.films.tests.utils import TestBaseFilm
from some_proj.films.tests.utils import check_200_status
from some_proj.films.tests.utils.comment.create_comment import create_comment
from some_proj.films.tests.utils.comment.delete_comment import delete_comments


class TestCommentsFilm(TestBaseFilm):
    def _get_response(self, user):
        self.client.force_authenticate(user=user)
        return self.client.get(
            reverse(
                "api:films-detail",
                kwargs={"pk": self.test_film.id},
            ),
        )

    def _check_not_empty_comments(self, user=None):
        response = self._get_response(user)
        self.assertTrue(
            response.data["comments"],
            f"Поле 'comments' не должно быть пустым {response.data['comments']}",
        )
        check_200_status(response)

    def _check_empty_comments(self, user):
        response = self._get_response(user)
        self.assertTrue(
            not response.data["comments"],
            f"Поле 'comments' должно быть пустым {response.data['comments']}",
        )
        check_200_status(response)

    # def _check_guest_comments(self):

    def test_check_default_admin_comments(self):
        self._check_empty_comments(self.test_admin)

    def test_check_add_admin_comments(self):
        create_comment(
            user=self.test_admin,
            content_id=self.test_film.id,
            model=FilmModel,
        )
        self._check_not_empty_comments(
            user=self.test_admin,
        )

    def test_check_delete_admin_comments(self):
        delete_comments(
            user=self.test_admin,
            content_id=self.test_film.id,
            model=FilmModel,
        )
        self._check_empty_comments(
            user=self.test_admin,
        )

    def test_check_default_auth_user_comments(self):
        self._check_empty_comments(
            user=self.test_auth_user,
        )

    def test_check_add_auth_user_comments(self):
        create_comment(
            user=self.test_auth_user,
            content_id=self.test_film.id,
            model=FilmModel,
        )
        self._check_not_empty_comments(
            user=self.test_auth_user,
        )

    def test_check_delete_auth_user_comments(self):
        delete_comments(
            user=self.test_auth_user,
            content_id=self.test_film.id,
            model=FilmModel,
        )
        self._check_empty_comments(
            user=self.test_auth_user,
        )
