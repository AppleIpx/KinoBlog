from rest_framework import serializers

from some_proj.films.models import ActorModel
from some_proj.media_for_kino_card.utils.shared_files import HTTPRemoverSerializer


class ActorSerializer(HTTPRemoverSerializer, serializers.ModelSerializer):
    class Meta:
        model = ActorModel
        fields = [
            "id",
            "name",
            "surname",
            "patronymic",
            "photo",
        ]
        fields_to_process = ["photo"]
