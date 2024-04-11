from some_proj.films.tests.factories import FilmFactory


def create_films(count):
    FilmFactory.create_batch(count)


def create_film():
    return FilmFactory.create()
