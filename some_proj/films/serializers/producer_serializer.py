from rest_framework import serializers

from some_proj.films.models import ProducerModel
from some_proj.media_for_kino_card.utils.shared_files import BaseHTTPRemoverSerializer


class ProducerSerializer(BaseHTTPRemoverSerializer, serializers.ModelSerializer):
    class Meta:
        model = ProducerModel
        fields = [
            "name",
            "surname",
            "patronymic",
            "photo",
        ]
        fields_to_process = ["photo"]
