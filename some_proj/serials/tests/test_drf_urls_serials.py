from django.urls import resolve
from django.urls import reverse

from some_proj.serials.models import SerialModel
from some_proj.serials.tests.utils.create_serials import create_serials


class TestSerialsUrl:
    def test_film_detail(self, serial: SerialModel):
        create_serials(10)
        assert reverse("api:serials-detail", kwargs={"pk": serial.pk}) == f"/api/serials/{serial.pk}/"
        assert resolve(f"/api/serials/{serial.pk}/").view_name == "api:serials-detail"

    def test_film_list(self):
        assert reverse("api:serials-list") == "/api/serials/"
        assert resolve("/api/serials/").view_name == "api:serials-list"
