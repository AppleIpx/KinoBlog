from some_proj.media_for_kino_card.models import Quality
from some_proj.media_for_kino_card.tasks import create_add_links_for_amazon
from some_proj.media_for_kino_card.utils.work_with_s3.defining_the_resolution import start_process_get_correlation
from some_proj.media_for_kino_card.utils.work_with_s3.download_from_s3 import download
from some_proj.media_for_kino_card.utils.work_with_s3.recoding_files import recoding
from some_proj.media_for_kino_card.utils.work_with_s3.upload_to_s3 import upload


# запуск всех процессов
def start_process_media_files_s3(instance):
    orig_file_path = instance.orig_path_file
    qualities = Quality.objects.all()

    # Скачивание файла с S3
    orig_local_path = download(
        orig_file_path,
        instance,
    )
    # Определение соотношения разрешения оригинального фильма
    correlation = start_process_get_correlation(
        orig_file_path,
    )
    # Кодирование видео
    recording_files_paths = recoding(
        instance,
        orig_local_path,
        qualities,
        correlation,
    )
    # Создание и добавление в таблицу ссылок видео-файлов на S3
    create_add_links_for_amazon.delay(
        instance,
        qualities,
        recording_files_paths,
    )
    # загрузка перекодированных фильмов на S3
    upload(
        recording_files_paths,
        f"{instance.film.name}/{instance.quality}",
    )
