from some_proj.media_for_kino_card.models import MediaFile


def updating_fields(instance):
    MediaFile.objects.filter(pk=instance.pk).update(
        episode=instance.episode,
        orig_path_file=instance.orig_path_file,
    )
