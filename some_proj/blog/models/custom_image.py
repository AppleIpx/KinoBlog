from django.db import models
from wagtail.blocks import CharBlock
from wagtail.blocks import ListBlock
from wagtail.blocks import StructBlock
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import AbstractImage
from wagtail.images.models import AbstractRendition
from wagtail.images.models import Image

from some_proj.contrib.mixins.add_bucket_in_url import AddBucketMixin
from some_proj.contrib.mixins.delete_http_in_url import DeleteHttpInUrlMixin
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


class CustomImageChoose(
    DeleteHttpInUrlMixin,
    AddBucketMixin,
    StructBlock,
):
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
        representation = super().get_api_representation(value, context)
        images = []
        title = value["title"]
        for image in value["image"]:
            image_data = ImageRenditionField("max-1920x1080|format-jpeg").to_representation(image)
            image_data_url = self.delete_http_in_url(image_data["url"])
            image_data_url = self.add_bucket_name(image_data_url, "photos")
            image_data["url"] = image_data_url
            image_data["full_url"] = image_data_url

            images.append(image_data)

        representation.update(
            {
                "images": images,
                "title": title,
            },
        )
        return representation
