from rest_framework import serializers

from CaCatHead.problem.serializers import ProblemSerializer, ProblemRepositorySerializer
from CaCatHead.submission.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    repository = ProblemRepositorySerializer(read_only=True)

    problem = ProblemSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'repository', 'problem', 'language', 'created', 'judged', 'verdict', 'score']


class FullSubmissionSerializer(serializers.ModelSerializer):
    repository = ProblemRepositorySerializer(read_only=True)

    problem = ProblemSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'repository', 'problem', 'code', 'language', 'created', 'judged', 'verdict', 'score', 'detail']
