import pytest

from some_proj.films.models import FilmModel
from some_proj.films.tests.factories import FilmFactory
from some_proj.serials.models import SerialModel
from some_proj.serials.tests.factories.serial import SerialFactory
from some_proj.users.models import User
from some_proj.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(db) -> User:
    return UserFactory()


@pytest.fixture()
def film(db) -> FilmModel:
    return FilmFactory()


@pytest.fixture()
def serial(db) -> SerialModel:
    return SerialFactory()
