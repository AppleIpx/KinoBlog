# Проверяется изменилась ли ссылка на исходное видео
def media_check_in_s3(previous_version, instance):
    return previous_version.url != instance.urls and previous_version
