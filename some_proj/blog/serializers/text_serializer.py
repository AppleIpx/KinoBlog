from rest_framework import serializers


class CustomTextBlockSerializer(serializers.Serializer):
    type = serializers.CharField()
    value = serializers.CharField()
