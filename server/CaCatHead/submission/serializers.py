from rest_framework import serializers

from CaCatHead.problem.serializers import ProblemSerializer, ProblemRepositorySerializer, PolygonProblemSerializer
from CaCatHead.submission.models import Submission
from CaCatHead.user.serializers import UserSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    repository = ProblemRepositorySerializer(read_only=True)

    problem = ProblemSerializer(read_only=True)

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'repository', 'problem', 'code_length', 'language', 'created', 'judged', 'verdict', 'score',
                  'owner']


class FullPolygonSubmissionSerializer(serializers.ModelSerializer):
    repository = ProblemRepositorySerializer(read_only=True)

    problem = PolygonProblemSerializer(read_only=True)

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'repository', 'problem', 'code', 'code_length', 'language', 'created', 'judged', 'verdict',
                  'score', 'detail', 'owner']


class FullSubmissionSerializer(serializers.ModelSerializer):
    repository = ProblemRepositorySerializer(read_only=True)

    problem = ProblemSerializer(read_only=True)

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'repository', 'problem', 'code', 'code_length', 'language', 'created', 'judged', 'verdict',
                  'score', 'detail', 'owner']
