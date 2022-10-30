from rest_framework import serializers
from rest_framework.exceptions import NotFound

from CaCatHead.problem.models import ProblemRepository, Problem


class CreateProblemPayload(serializers.Serializer):
    title = serializers.CharField(max_length=512)
    display_id = serializers.IntegerField(allow_null=True, required=False)


class ProblemRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemRepository
        fields = ['id', 'name', 'is_public']


class BaseProblemSerializer(serializers.ModelSerializer):
    def get_or_raise(self):
        """
        检查待序列化的 Post 对象是否为空, 抛出 404
        """
        if self.instance is not None:
            return self.data
        else:
            raise NotFound(detail='题目未找到')


class ProblemSerializer(BaseProblemSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'display_id', 'title']
