def get_film_names(cadrs_films):
    film_names = set()
    for photo in cadrs_films.all():
        film_names.add(photo.film.name)
    return film_names


def get_serial_names(cadrs_serials):
    serial_names = set()
    for photo in cadrs_serials.all():
        serial_names.add(photo.serial.name)
    return serial_names


def cadrs_check(cadrs_films, cadrs_serials):
    film_names = get_film_names(cadrs_films)
    serial_names = get_serial_names(cadrs_serials)

    if film_names and not serial_names:
        names_str = ", ".join(film_names)
        return f"кадры из фильма: {names_str}"

    if serial_names and not film_names:
        names_str = ", ".join(serial_names)
        return f"кадры из сериала: {names_str}"

    if film_names and serial_names:
        film_name = film_names.pop()
        serial_name = serial_names.pop()
        return f"кадры из {film_name} и {serial_name}"

    return "Пустые кадры"
