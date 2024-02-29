from django.apps import AppConfig


class MediaForKinoCardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "some_proj.media_for_kino_card"

    def ready(self):
        pass
