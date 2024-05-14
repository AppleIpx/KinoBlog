from rest_framework import serializers

from some_proj.films.models import ActorModel


class ActorSerializer(serializers.ModelSerializer):
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
