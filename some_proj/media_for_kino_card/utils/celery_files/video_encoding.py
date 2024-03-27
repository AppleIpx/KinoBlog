import logging

from some_proj.media_for_kino_card.tasks import recoding_files


def encoding(orig_local_path_value, content_name, quality, correlation_value):
    recording_start_message = f"Начало кодирования качества {quality.name}"
    logging.info(recording_start_message)

    # Кодирование видео
    recording_file_path = recoding_files.delay(
        orig_local_path_value,
        content_name,
        quality.name,
        correlation_value,
    )
    recording_file_path_value = recording_file_path.get(propagate=False)
    success_msg_recording = f"Кодирование качества {quality.name} прошло успешно"
    logging.info(success_msg_recording)
    return recording_file_path_value
