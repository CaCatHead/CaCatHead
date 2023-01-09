from rest_framework import serializers

from CaCatHead.judge.models import JudgeNode


class JudgeNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JudgeNode
        fields = ['name', 'active', 'updated', 'information']
