from rest_framework import serializers
from wagtail.blocks import StreamValue

from some_proj.blog.serializers.cadrs_serializer import CadrsBlogSerializer
from some_proj.blog.serializers.embed_serializer import EmbedBlockSerializer
from some_proj.blog.serializers.film_blog_serializer import WidgetFilmBlogSerializer
from some_proj.blog.serializers.image_seializer import CustomImageBlockSerializer
from some_proj.blog.serializers.serial_blog_serializer import WidgetSerialBlogSerializer


class StreamFieldSerializer(serializers.Field):
    SERIALIZERS = {
        "text": lambda block: block.value.source,
        "image": lambda block: CustomImageBlockSerializer(block.value).data,
        "content": lambda block: EmbedBlockSerializer(block.value).data,
        "film": lambda block: WidgetFilmBlogSerializer(block.value, read_only=True).data,
        "serial": lambda block: WidgetSerialBlogSerializer(block.value, read_only=True).data,
        "cadrs": lambda block: CadrsBlogSerializer(block.value, read_only=True).data,
    }

    def to_representation(self, value):
        if isinstance(value, StreamValue):
            blocks = []
            for block in value:
                block_data = {
                    "type": block.block_type,
                    "value": self.SERIALIZERS.get(block.block_type, lambda b: b.value)(block),
                }
                blocks.append(block_data)
            return blocks
        return None
