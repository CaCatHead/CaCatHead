from rest_framework import serializers
from rest_framework.exceptions import NotFound

from CaCatHead.problem.models import ProblemRepository, Problem, ProblemInfo, ProblemContent, ProblemJudge


class CreateProblemPayload(serializers.Serializer):
    title = serializers.CharField(max_length=512)
    display_id = serializers.IntegerField(allow_null=True, required=False)


class EditProblemPayload(serializers.Serializer):
    title = serializers.CharField(max_length=512, allow_blank=True, required=False)
    display_id = serializers.IntegerField(required=False)
    time_limit = serializers.IntegerField(required=False)
    memory_limit = serializers.IntegerField(required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    input = serializers.CharField(allow_blank=True, required=False)
    output = serializers.CharField(allow_blank=True, required=False)
    sample = serializers.JSONField(required=False)
    hint = serializers.CharField(allow_blank=True, required=False)
    source = serializers.CharField(allow_blank=True, required=False)
    extra_content = serializers.JSONField(required=False)
    extra_judge = serializers.JSONField(required=False)


class EditPermissionPayload(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    group_id = serializers.IntegerField(required=False)
    grant = serializers.CharField(max_length=32, required=False)
    revoke = serializers.CharField(max_length=32, required=False)


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
        fields = ['display_id', 'title', 'problem_type', 'is_public']


class _ProblemContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemContent
        fields = ['title', 'description', 'input', 'output', 'sample', 'hint', 'source', 'extra_content']


class _ProblemJudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemJudge
        fields = ['problem_type', 'time_limit', 'memory_limit', 'score', 'testcase_count', 'testcase_detail',
                  'extra_info']


class FullProblemInfoSerializer(serializers.ModelSerializer):
    problem_content = _ProblemContentSerializer(read_only=True)
    problem_judge = _ProblemJudgeSerializer(read_only=True)

    class Meta:
        model = ProblemInfo
        fields = ['problem_content', 'problem_judge']


class FullProblemSerializer(BaseProblemSerializer):
    problem_info = FullProblemInfoSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = ['id', 'display_id', 'title', 'problem_type', 'time_limit', 'memory_limit', 'is_public',
                  'problem_info']


class ProblemInfoContentSerializer(serializers.ModelSerializer):
    problem_content = _ProblemContentSerializer(read_only=True)

    class Meta:
        model = ProblemInfo
        fields = ['problem_content']


class ProblemContentSerializer(BaseProblemSerializer):
    problem_info = ProblemInfoContentSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = ['display_id', 'title', 'problem_type', 'time_limit', 'memory_limit', 'is_public', 'problem_info']
