from rest_framework import serializers

from some_proj.films.models import CountryModel


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryModel
        fields = ["name"]
