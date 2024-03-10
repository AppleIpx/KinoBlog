from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from some_proj.films.models import FilmContentModel
from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.utils.executing_processes_in_signal import start_signal_processes
from some_proj.serials.models import SerialModel


@receiver(post_save, sender=SerialModel)
@receiver(post_save, sender=FilmContentModel)
def create_media_file(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)
    if created:
        MediaFile.objects.create(content_type=content_type, object_id=instance.id)


@receiver(pre_save, sender=MediaFile)
def update_media_file(sender, instance, **kwargs):
    if instance.pk:
        start_signal_processes(instance)
