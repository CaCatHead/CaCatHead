from rest_framework import serializers
from rest_framework.exceptions import NotFound

from CaCatHead.problem.models import ProblemRepository, Problem, ProblemInfo, ProblemContent, ProblemJudge


class CreateProblemPayload(serializers.Serializer):
    title = serializers.CharField(max_length=512)
    display_id = serializers.IntegerField(allow_null=True, required=False)


class EditProblemPayload(serializers.Serializer):
    title = serializers.CharField(max_length=512, required=False)
    display_id = serializers.IntegerField(required=False)
    time_limit = serializers.IntegerField(required=False)
    memory_limit = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    input = serializers.CharField(required=False)
    output = serializers.CharField(required=False)
    sample = serializers.CharField(required=False)
    hint = serializers.CharField(required=False)
    source = serializers.CharField(required=False)
    extra_content = serializers.CharField(required=False)


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


class ProblemContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemContent
        fields = ['title', 'description', 'input', 'output', 'sample', 'hint', 'source', 'extra_content']


class ProblemJudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemJudge
        fields = ['time_limit', 'memory_limit', 'score', 'testdata_count', 'testdata_score', 'extra_info']


class ProblemInfoSerializer(serializers.ModelSerializer):
    problem_content = ProblemContentSerializer(read_only=True)
    problem_judge = ProblemJudgeSerializer(read_only=True)

    class Meta:
        model = ProblemInfo
        fields = ['problem_content', 'problem_judge']


class FullProblemSerializer(BaseProblemSerializer):
    problem_info = ProblemInfoSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = ['id', 'display_id', 'title', 'time_limit', 'memory_limit', 'problem_info']