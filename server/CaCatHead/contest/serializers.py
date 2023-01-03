from rest_framework import serializers

from CaCatHead.contest.models import Contest


class CreateContestPayloadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)

    type = serializers.CharField(max_length=64)


class EditContestPayloadSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_null=True, max_length=256)

    start_time = serializers.DateTimeField(required=False, allow_null=True)

    freeze_time = serializers.DateTimeField(required=False, allow_null=True)

    end_time = serializers.DateTimeField(required=False, allow_null=True)

    password = serializers.CharField(required=False, allow_null=True, max_length=256)

    is_public = serializers.BooleanField(required=False, allow_null=True)


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['id', 'title', 'type', 'start_time', 'freeze_time', 'end_time', 'is_public']
