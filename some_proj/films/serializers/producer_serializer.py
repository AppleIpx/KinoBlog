from rest_framework import serializers

from some_proj.films.models import ProducerModel


class ProducerSerializer(serializers.ModelSerializer):
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
