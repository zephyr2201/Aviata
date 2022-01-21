from rest_framework import serializers


class ResultReadSerializer(serializers.Serializer):
    data = serializers.JSONField()
