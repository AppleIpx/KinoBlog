from django.urls import resolve
from django.urls import reverse

from some_proj.films.models import FilmModel
from some_proj.films.tests.utils.create_films import create_films


class TestFilmsUrl:
    def test_film_detail(self, film: FilmModel):
        create_films(10)
        assert reverse("api:films-detail", kwargs={"pk": film.pk}) == f"/api/films/{film.pk}/"
        assert resolve(f"/api/films/{film.pk}/").view_name == "api:films-detail"

    def test_film_list(self):
        assert reverse("api:films-list") == "/api/films/"
        assert resolve("/api/films/").view_name == "api:films-list"
