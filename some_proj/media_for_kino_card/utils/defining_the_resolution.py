from some_proj.media_for_kino_card.tasks import get_video_stream


def get_correlation(width, height):
    return int(width) / int(height)


def start_process_get_correlation(filepath):
    width, height = get_video_stream.delay(filepath)
    return get_correlation(width, height)
