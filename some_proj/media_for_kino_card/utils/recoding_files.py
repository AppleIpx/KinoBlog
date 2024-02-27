from some_proj.media_for_kino_card.tasks import recoding_files


def recoding(instance, orig_local_path, qualities):
    # Перекодирование исходного файла в 4 качества
    return [
        recoding_files.delay(
            orig_local_path,
            instance.film.name,
            quality.name,
        )
        for quality in qualities
    ]
