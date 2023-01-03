from rest_framework import serializers


class CreateContestPayloadSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=256)

    type = serializers.CharField(max_length=64)
