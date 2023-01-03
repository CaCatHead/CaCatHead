from rest_framework import serializers

from CaCatHead.contest.models import Contest


class CreateContestPayloadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)

    type = serializers.CharField(max_length=64)


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['title', 'type', 'start_time', 'freeze_time', 'end_time', 'is_public']
