from rest_framework import serializers

from CaCatHead.problem.models import ProblemRepository, Problem


class ProblemRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemRepository
        fields = ['id', 'name', 'is_public']


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'display_id', 'title', 'time_limit', 'memory_limit']
