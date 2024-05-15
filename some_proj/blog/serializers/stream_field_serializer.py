from rest_framework import serializers
from wagtail.blocks import StreamValue


class StreamFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, StreamValue):
            blocks = []
            for block in value:
                block_type = block.block_type
                block_value = block.value
                api_representation = block.block.get_api_representation(block_value, self.context)
                blocks.append({"type": block_type, "value": api_representation})
            return blocks
        return None
