import pytest
from django.urls import reverse

from some_proj.films.tests.utils import check_200_status
from some_proj.films.tests.utils.watch.create_watch import create_watch
from some_proj.films.tests.utils.watch.delete_watch import delete_watch
from some_proj.serials.models import SerialModel
from some_proj.serials.tests.utils.base_test_serial import TestBaseSerial


@pytest.mark.django_db()
class TestWatchFilms(TestBaseSerial):
    def _check_watch_status(self, user, expected_value):
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse(
                "api:serials-detail",
                kwargs={"pk": self.test_serial.id},
            ),
        )
        check_200_status(response)
        self.assertEqual(
            response.data["is_watched"],
            expected_value,
            f"Должно было быть {expected_value}",
        )

    def test_check_default_admin_watch(self):
        self._check_watch_status(user=self.test_admin, expected_value=False)

    def test_check_add_admin_watch(self):
        create_watch(
            self.test_admin,
            self.test_serial.id,
            SerialModel,
        )
        self._check_watch_status(
            user=self.test_admin,
            expected_value=True,
        )

    def test_check_delete_admin_watch(self):
        delete_watch(
            self.test_admin,
            self.test_serial.id,
            SerialModel,
        )
        self._check_watch_status(
            user=self.test_admin,
            expected_value=False,
        )

    def test_check_default_auth_user_watch(self):
        self._check_watch_status(
            user=self.test_auth_user,
            expected_value=False,
        )

    def test_check_add_auth_user_watch(self):
        create_watch(
            self.test_auth_user,
            self.test_serial.id,
            SerialModel,
        )
        self._check_watch_status(
            user=self.test_auth_user,
            expected_value=True,
        )

    def test_check_delete_auth_user_watch(self):
        delete_watch(
            self.test_auth_user,
            self.test_serial.id,
            SerialModel,
        )
        self._check_watch_status(
            user=self.test_auth_user,
            expected_value=False,
        )
