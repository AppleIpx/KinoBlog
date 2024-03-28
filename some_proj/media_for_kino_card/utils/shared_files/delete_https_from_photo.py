from django.conf import settings
from rest_framework import serializers


class HTTPRemoverSerializer(serializers.ModelSerializer):
    def remove_extra_https(self, data, fields):
        for field in fields:
            if field in data:
                if isinstance(data[field], str) and data[field].startswith("https://"):
                    data[field] = data[field].replace("https://", "", 1)
                elif isinstance(data[field], dict):
                    self.remove_extra_https(data[field], data[field].keys())
        return data

    def add_bucket_name(self, data, fields):
        bucket_name = f"{settings.AWS_STORAGE_BUCKET_NAME}/"
        for field in fields:
            if field in data:
                if isinstance(data[field], str) and "photos" in data[field]:
                    data[field] = data[field].replace("photos", f"{bucket_name}photos", 1)
                elif isinstance(data[field], dict):
                    self.add_bucket_name(data[field], data[field].keys())
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        fields_to_process = getattr(self.Meta, "fields_to_process", [])
        representation = self.remove_extra_https(representation, fields_to_process)
        return self.add_bucket_name(representation, fields_to_process)
