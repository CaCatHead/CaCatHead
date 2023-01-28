from rest_framework import serializers

from CaCatHead.contest.models import Contest, ContestRegistration, Team, RatingLog
from CaCatHead.problem.serializers import ProblemContentSerializer
from CaCatHead.user.serializers import UserSerializer


class CreateContestPayloadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)

    type = serializers.CharField(max_length=64)


class EditContestPayloadSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_null=True, max_length=64)

    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    start_time = serializers.DateTimeField(required=False, allow_null=True)

    freeze_time = serializers.DateTimeField(required=False, allow_null=True)

    end_time = serializers.DateTimeField(required=False, allow_null=True)

    password = serializers.CharField(required=False, allow_null=True, max_length=256)

    is_public = serializers.BooleanField(required=False, allow_null=True)

    problems = serializers.ListSerializer(child=serializers.IntegerField(), required=False, allow_null=True,
                                          allow_empty=True)

    view_standings = serializers.BooleanField(required=False, allow_null=True)

    view_submissions_after_contest = serializers.BooleanField(required=False, allow_null=True)

    view_submission_checker_info = serializers.BooleanField(required=False, allow_null=True)


class UserRegisterPayloadSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True, max_length=32)

    password = serializers.CharField(required=False, allow_null=True, max_length=256)

    extra_info = serializers.JSONField(required=False, allow_null=True)


class ContestSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Contest
        fields = ['id', 'title', 'type', 'start_time', 'freeze_time', 'end_time', 'is_public', 'owner']


class ContestContentSerializer(serializers.BaseSerializer):
    def to_representation(self, contest: Contest):
        return {
            'id': contest.id,
            'title': contest.title,
            'type': contest.type,
            'start_time': contest.start_time,
            'freeze_time': contest.freeze_time,
            'end_time': contest.end_time,
            'is_public': contest.is_public,
            'settings': contest.settings,
            'owner': UserSerializer(contest.owner).data,
            'description': contest.description,
            'problems': ProblemContentSerializer(contest.problem_repository.problems, many=True).data
        }


class TeamSerializer(serializers.BaseSerializer):
    def to_representation(self, team: Team):
        return {
            'name': team.name,
            'owner': UserSerializer(team.owner).data,
            'members': UserSerializer(team.members, many=True).data,
            'created': team.created,
        }


class ContestRegistrationSerializer(serializers.BaseSerializer):
    def to_representation(self, registration: ContestRegistration):
        return {
            'name': registration.name,
            'team': TeamSerializer(registration.team).data,
            'created': registration.created,
            'extra_info': registration.extra_info
        }


class ContestStandingSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = ContestRegistration
        fields = ['name', 'team', 'created', 'score', 'dirty', 'standings', 'is_participate', 'extra_info']


class RatingLogSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    old_rating = serializers.SerializerMethodField(method_name='get_old_rating')

    class Meta:
        model = RatingLog
        fields = ['contest_id', 'team', 'old_rating', 'delta', 'created']

    def get_old_rating(self, obj: RatingLog):
        return obj.rating
