from some_proj.media_for_kino_card.tasks import upload_to_s3


def upload(recording_files_paths, file_name):
    # имя файла
    return upload_to_s3.delay(recording_files_paths, file_name)
