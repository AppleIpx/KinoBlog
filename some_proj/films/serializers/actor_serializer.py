from rest_framework import serializers

from some_proj.films.models import ActorModel
from some_proj.media_for_kino_card.utils.shared_files import BaseHTTPRemoverSerializer


class ActorSerializer(BaseHTTPRemoverSerializer, serializers.ModelSerializer):
    class Meta:
        model = ActorModel
        fields = [
            "name",
            "surname",
            "patronymic",
            "photo",
        ]
        fields_to_process = ["photo"]
