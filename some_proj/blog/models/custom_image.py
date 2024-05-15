from django.db import models
from wagtail.blocks import CharBlock
from wagtail.blocks import ListBlock
from wagtail.blocks import StructBlock
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import AbstractImage
from wagtail.images.models import AbstractRendition
from wagtail.images.models import Image

from some_proj.media_for_kino_card.utils.shared_files import generate_filename_photos


class CustomImage(AbstractImage):
    admin_form_fields = Image.admin_form_fields

    @classmethod
    def get_rendition_model(cls):
        return CustomRendition

    def get_upload_to(self, filename):
        return filename


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    def get_upload_to(self, filename):
        return generate_filename_photos(self, filename)

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class CustomImageChoose(StructBlock):
    image = ListBlock(
        ImageChooserBlock(
            label="Изображение",
            icon="image",
            help_text="Загрузите изображение",
        ),
    )
    title = CharBlock(
        blank=True,
        label="Заголовок",
        required=False,
    )
    description = CharBlock(
        blank=True,
        label="Описание",
        required=False,
    )

    class Meta:
        label = "Изображение"

    def get_api_representation(self, value, context=None):
        super().get_api_representation(value, context)
        images = []
        for image in value["image"]:
            photo = {
                "id": image.id,
                "image": ImageRenditionField("max-1920x1080|format-jpeg").to_representation(image),
                "image_tags": [{"id": tag.id, "name": tag.name} for tag in image.tags.all()],
            }
            images.append(photo)
        return {
            "title": value["title"],
            "images": images,
        }
