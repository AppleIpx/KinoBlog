from some_proj.media_for_kino_card.tasks import recoding_files


def recoding(film_name, orig_file_path, qualities, correlation):
    # Перекодирование исходного файла в 4 качества
    return [
        recoding_files(
            orig_file_path,
            film_name,
            quality.name,
            correlation,
        )
        for quality in qualities
    ]
