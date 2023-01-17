from rest_framework import serializers

from CaCatHead.contest.serializers import TeamSerializer
from CaCatHead.problem.serializers import ProblemSerializer, ProblemRepositorySerializer, PolygonProblemSerializer
from CaCatHead.submission.models import Submission, ContestSubmission
from CaCatHead.user.serializers import UserSerializer


class SubmitCodePayload(serializers.Serializer):
    code = serializers.CharField(max_length=65535, required=True)
    language = serializers.ChoiceField(choices=('c', 'cpp', 'java'), required=True)


class SubmissionSerializer(serializers.ModelSerializer):
    repository = ProblemRepositorySerializer(read_only=True)

    problem = ProblemSerializer(read_only=True)

    owner = UserSerializer(read_only=True)

    judge_node = serializers.SerializerMethodField(method_name='get_judge_node')

    class Meta:
        model = Submission
        fields = ['id', 'repository', 'problem', 'code_length', 'language', 'created', 'judged', 'verdict',
                  'score', 'time_used', 'memory_used', 'judge_node', 'owner']

    def get_judge_node(self, obj: Submission):
        if 'node' in obj.detail:
            return obj.detail['node']
        else:
            return None


class ContestSubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer(read_only=True)

    owner = TeamSerializer(read_only=True)

    class Meta:
        model = ContestSubmission
        fields = ['id', 'type', 'problem', 'code_length', 'language', 'created', 'judged', 'relative_time', 'verdict',
                  'score', 'time_used', 'memory_used', 'owner']


class FullContestSubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer(read_only=True)

    owner = TeamSerializer(read_only=True)

    class Meta:
        model = ContestSubmission
        fields = ['id', 'type', 'problem', 'code', 'code_length', 'language', 'created', 'judged', 'relative_time',
                  'verdict', 'score', 'detail', 'time_used', 'memory_used', 'owner']


class NoDetailContestSubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer(read_only=True)

    owner = TeamSerializer(read_only=True)

    detail = serializers.SerializerMethodField(method_name='get_detail')

    class Meta:
        model = ContestSubmission
        fields = ['id', 'type', 'problem', 'code', 'code_length', 'language', 'created', 'judged', 'relative_time',
                  'verdict', 'score', 'detail', 'time_used', 'memory_used', 'owner']

    def get_detail(self, sub: ContestSubmission):
        if 'results' in sub.detail:
            results = filter(lambda t: 'sample' in t and bool(t['sample']), sub.detail['results'])
            sub.detail['results'] = results
            return sub.detail
        else:
            return sub.detail


class FullPolygonSubmissionSerializer(serializers.ModelSerializer):
    repository = ProblemRepositorySerializer(read_only=True)

    problem = PolygonProblemSerializer(read_only=True)

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'repository', 'problem', 'code', 'code_length', 'language', 'created', 'judged', 'verdict',
                  'score', 'detail', 'time_used', 'memory_used', 'owner']


class FullSubmissionSerializer(serializers.ModelSerializer):
    repository = ProblemRepositorySerializer(read_only=True)

    problem = ProblemSerializer(read_only=True)

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'repository', 'problem', 'code', 'code_length', 'language', 'created', 'judged', 'verdict',
                  'score', 'detail', 'time_used', 'memory_used', 'owner']
