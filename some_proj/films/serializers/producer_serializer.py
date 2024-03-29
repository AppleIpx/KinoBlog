from rest_framework import serializers

from some_proj.films.models import ProducerModel
from some_proj.media_for_kino_card.utils.shared_files import HTTPRemoverSerializer


class ProducerSerializer(HTTPRemoverSerializer, serializers.ModelSerializer):
    class Meta:
        model = ProducerModel
        fields = [
            "id",
            "name",
            "surname",
            "patronymic",
            "photo",
        ]
        fields_to_process = ["photo"]
