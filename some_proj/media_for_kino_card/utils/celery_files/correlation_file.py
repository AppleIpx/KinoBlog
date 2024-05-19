import logging

from some_proj.media_for_kino_card.tasks import get_video_stream


def get_correlation(orig_local_path_value):
    correlation_start_message = "Определяется соотношение исходного файла"
    logging.info(correlation_start_message)

    # Определение соотношения разрешения оригинального фильма
    correlation = get_video_stream(
        orig_local_path_value,
    )
    correlation_value = correlation.get(timeout=60)

    correlation_message = "Соотношение определено"
    logging.info(correlation_message)
    return correlation_value
