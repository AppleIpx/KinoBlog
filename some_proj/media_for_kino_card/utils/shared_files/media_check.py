# Проверяется изменилась ли ссылка на исходное видео
import logging


def check_change_urls(previous_version, instance):
    if previous_version.orig_path_file != instance.orig_path_file:
        info_message = "Ссылка на исходных файл была изменена"
        logging.info(info_message)
        return True
    url_info = "Ссылка на исходный файл не изменена, кодирование не требуется"
    logging.info(url_info)
    return False
