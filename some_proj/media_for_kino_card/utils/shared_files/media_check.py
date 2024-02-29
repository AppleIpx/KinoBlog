# Проверяется изменилась ли ссылка на исходное видео
def check_change_urls(previous_version, instance):
    return previous_version.orig_path_file != instance.orig_path_file
