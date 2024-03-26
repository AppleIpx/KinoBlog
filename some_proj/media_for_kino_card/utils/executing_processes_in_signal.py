import logging

from some_proj.media_for_kino_card.utils.s3_files import check_env_files
from some_proj.media_for_kino_card.utils.shared_files import check_urls
from some_proj.media_for_kino_card.utils.shared_files import update_media
from some_proj.media_for_kino_card.utils.starting_processes import start_local
from some_proj.media_for_kino_card.utils.starting_processes import start_s3


def start_signal_processes(instance):
    try:
        # получение предыдущего экземпляра медии
        previous_version = instance.history.first()

        # проверка на изменение исходного пути
        if check_urls(previous_version, instance):
            # проверка на имеющиеся переменные для S3
            if check_env_files():
                # запуск всех процессов с S3
                start_s3(instance)
            else:
                # запуск всех процессов локально
                start_local(instance)
        # обновление полей медии
        update_media(instance)
    except Exception as e:
        message_error = f"В выполнении сигнала произошла ошибка: {e}"
        logging.exception(message_error)
    else:
        successful_message = "Все процессы в сигнале выполнены успешно"
        logging.info(successful_message)
