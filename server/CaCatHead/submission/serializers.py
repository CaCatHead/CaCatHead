from rest_framework import serializers

from CaCatHead.contest.serializers import TeamSerializer
from CaCatHead.problem.serializers import ProblemSerializer, ProblemRepositorySerializer, PolygonProblemSerializer
from CaCatHead.submission.models import Submission, ContestSubmission
from CaCatHead.user.serializers import UserSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    repository = ProblemRepositorySerializer(read_only=True)

    problem = ProblemSerializer(read_only=True)

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'repository', 'problem', 'code_length', 'language', 'created', 'judged', 'verdict',
                  'score', 'time_used', 'memory_used', 'owner']


class ContestSubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer(read_only=True)

    owner = TeamSerializer(read_only=True)

    class Meta:
        model = ContestSubmission
        fields = ['id', 'type', 'problem', 'code_length', 'language', 'created', 'judged', 'relative_time', 'verdict',
                  'score', 'time_used', 'memory_used', 'owner']


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
