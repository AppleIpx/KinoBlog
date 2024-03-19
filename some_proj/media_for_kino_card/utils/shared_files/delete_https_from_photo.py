from rest_framework import serializers


class BaseHTTPRemoverSerializer(serializers.ModelSerializer):
    def remove_extra_https(self, data, fields):
        for field in fields:
            if field in data and data[field].startswith("https://"):
                data[field] = data[field].replace("https://", "", 1)
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        fields_to_process = getattr(self.Meta, "fields_to_process", [])
        return self.remove_extra_https(representation, fields_to_process)
