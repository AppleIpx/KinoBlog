import logging

from some_proj.media_for_kino_card.utils.local_work.start_all_process_local import start_process_media_files_local
from some_proj.media_for_kino_card.utils.shared_files.check_env_files_for_s3 import check_env_files
from some_proj.media_for_kino_card.utils.shared_files.check_history_media import get_previous_media
from some_proj.media_for_kino_card.utils.shared_files.media_check import check_change_urls
from some_proj.media_for_kino_card.utils.shared_files.updating_fields_media import updating_fields
from some_proj.media_for_kino_card.utils.work_with_s3.start_all_process_s3 import start_process_media_files_s3


def start_signal_processes(instance):
    try:
        # получение предыдущего экземпляра медии
        previous_version = get_previous_media(instance)
        # проверка на изменение исходного пути
        if check_change_urls(previous_version, instance):
            info_message = "Ссылка на исходных файл была изменена"
            logging.info(info_message)
            # проверка на имеющиеся переменные для S3
            if check_env_files():
                logging.info("Переменные для подключения к S3 обнаружены")
                # запуск всех процессов с S3
                start_process_media_files_s3(previous_version)
            else:
                warning_message = "Необходимо установить переменные окружения для подключения к S3."
                logging.warning(warning_message)
                # запуск всех процессов локально
                start_process_media_files_local(instance)
        logging.info("Ссылка не изменена, кодирование не требуется")
        # обновление полей медии
        updating_fields(instance)
    except Exception as e:
        message_error = f"В выполнении сигнала произошла ошибка: {e}"
        logging.exception(message_error)
    else:
        successful_message = "Все процессы в сигнале выполнены успешно"
        logging.info(successful_message)
