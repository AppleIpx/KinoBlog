from pathlib import Path
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from some_proj.films.models import FilmModel
from some_proj.films.models import MediaFile
from some_proj.films.tests.utils.conversion_video.get_quality_in_video import get_quality
from some_proj.films.tests.utils.create_films import create_film
from some_proj.films.tests.utils.media_files.create_media_files import create_media
from some_proj.media_for_kino_card.models import Quality
from some_proj.media_for_kino_card.tasks import recoding_files
from some_proj.media_for_kino_card.utils.celery_files import get_correlation
from some_proj.media_for_kino_card.utils.shared_files import create_add_links
from some_proj.media_for_kino_card.utils.shared_files import generate_path


class TestFilmSignals(TestCase):
    orig_local_path = "/Users/Eugeniy/Downloads/short_nigth_city.mp4"
    qualities = Quality.objects.all()
    content_name = "tests/test_file"
    local_files_paths = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.film = create_film()

    def test_media_file_creation_on_post_save(self):
        self.assertEqual(MediaFile.objects.count(), 1)
        media_file_film = MediaFile.objects.get(object_id=self.film.id)
        self.assertEqual(media_file_film.content_type, ContentType.objects.get_for_model(FilmModel))

    @patch("some_proj.media_for_kino_card.signals.start_signal_processes")
    def test_pre_save_signal_for_media_file(self, mock_start_signal_processes):
        media_file = create_media(FilmModel, self.film.id)

        media_file.orig_path_file = "new value"
        media_file.save()

        mock_start_signal_processes.assert_called()

    @patch("some_proj.media_for_kino_card.signals.start_signal_processes")
    def test_pre_save_signal_saves_updated_orig_path_file(self, mock_start_signal_processes):
        self.media_file = create_media(FilmModel, self.film.id)

        new_value = "new value"
        self.media_file.orig_path_file = new_value
        self.media_file.save()

        self.media_file.refresh_from_db()

        mock_start_signal_processes.assert_called()
        self.assertEqual(self.media_file.orig_path_file, new_value)

    def test_get_correlation(self):
        self.correlation_value = get_correlation(self.orig_local_path)
        self.assertEqual(self.correlation_value, 1920 / 1080, self.correlation_value)

    def test_recording(self):
        for quality in self.qualities:
            recoding_files(
                self.orig_local_path,
                self.content_name,
                quality,
                self.correlation_value,
            )
            output_folder = Path(generate_path(self.content_name))
            output_file = output_folder / f"{quality}.mp4"
            self.local_files_paths.append(output_file)
            self.assertTrue(output_file.exists(), f"Файл {output_file} не существует")

    def test_check_recorded_files(self):
        for path, quality in zip(self.local_files_paths, self.qualities, strict=False):
            video_quality = get_quality(path)
            self.assertEqual(video_quality, quality, f"ожидалось {quality}, а пришло {video_quality}")

    def test_check_create_links(self):
        for path, quality in zip(self.local_files_paths, self.qualities, strict=False):
            link = create_add_links(self.media_file, quality, path)
            self.assertEqual(link.url_media, path, f"ожидался следующий путь: {link.url_media}")
