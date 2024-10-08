from django.contrib.auth.models import User, Group
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes, throttle_classes
from rest_framework.exceptions import NotFound
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.views import APIView

from CaCatHead.core.decorators import HasPolygonPermission, func_validate_request, class_validate_request, \
    SubmitRateThrottle
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.permission.constants import ProblemPermissions
from CaCatHead.permission.serializers import UserPermissionSerializer, GroupPermissionSerializer
from CaCatHead.problem.models import Problem, DefaultCheckers
from CaCatHead.problem.serializers import CreateProblemPayload, \
    EditProblemPayload, FullProblemSerializer, EditPermissionPayload, PolygonProblemSerializer, \
    SubmitCheckerPayload
from CaCatHead.problem.views.services import make_problem, edit_problem, get_main_problem_repo, \
    make_problem_by_uploading, edit_problem_by_uploading, upload_custom_checker
from CaCatHead.problem.views.submit import submit_polygon_problem_code, \
    rejudge_polygon_problem_code
from CaCatHead.problem.views.upload import ProblemDirectory
from CaCatHead.submission.models import Submission
from CaCatHead.submission.serializers import FullSubmissionSerializer, SubmissionSerializer, \
    FullPolygonSubmissionSerializer, SubmitCodePayload
from CaCatHead.utils import make_response, make_error_response


# ----- Polygon -----
@api_view(['POST'])
@permission_classes([HasPolygonPermission])
@func_validate_request(CreateProblemPayload)
def create_problem(request: Request):
    """
    创建题目
    """
    title = request.data['title']
    display_id = request.data.get('display_id', None)
    problem = make_problem(title=title, user=request.user, display_id=display_id)
    return make_response(problem=PolygonProblemSerializer(problem).data)


@api_view(['POST'])
@permission_classes([HasPolygonPermission])
@parser_classes([FileUploadParser])
def upload_problem(request: Request):
    """
    上传题目
    """
    zip_file = request.data['file']
    problem = make_problem_by_uploading(zip_file, user=request.user)
    return make_response(problem=FullProblemSerializer(problem).get_or_raise())


@api_view(['POST'])
@permission_classes([HasPolygonPermission])
@parser_classes([FileUploadParser])
def edit_polygon_problem_by_upload(request: Request, problem_id: int):
    """
    上传题目压缩包更新题目
    """
    problem = Problem.objects.filter_user_permission(problemrepository=get_main_problem_repo(),
                                                     display_id=problem_id,
                                                     user=request.user,
                                                     permission=ProblemPermissions.Edit).first()
    if problem is None:
        raise NotFound('题目未找到')
    else:
        zip_file = request.data['file']
        problem = edit_problem_by_uploading(zip_file, problem=problem)
        return make_response(problem=FullProblemSerializer(problem).get_or_raise())


@api_view(['POST'])
@permission_classes([HasPolygonPermission])
@func_validate_request(EditProblemPayload)
def edit_polygon_problem(request: Request, problem_id: int):
    """
    编辑自己创建的题目, 或者被授予编辑权限的题目
    """
    problem = Problem.objects.filter_user_permission(problemrepository=get_main_problem_repo(),
                                                     display_id=problem_id,
                                                     user=request.user,
                                                     permission=ProblemPermissions.Edit).first()
    if problem is None:
        raise NotFound('题目未找到')
    else:
        problem = edit_problem(problem=problem, payload=request.data)
        return make_response(problem=FullProblemSerializer(problem).get_or_raise())


@api_view(['POST'])
@permission_classes([HasPolygonPermission])
@func_validate_request(SubmitCheckerPayload)
def upload_polygon_problem_checker(request: Request, problem_id: int):
    """
    编辑自己创建的题目, 或者被授予编辑权限的题目
    """
    problem = Problem.objects.filter_user_permission(problemrepository=get_main_problem_repo(),
                                                     display_id=problem_id,
                                                     user=request.user,
                                                     permission=ProblemPermissions.Edit).first()
    if problem is None:
        raise NotFound('题目未找到')
    else:
        checker_type = request.data['type']
        if checker_type == DefaultCheckers.custom:
            code = request.data['code'] if 'code' in request.data else None
            language = request.data['language'] if 'language' in request.data else None
            if code is None or len(code) == 0:
                raise BadRequest(detail='Checker 代码不能为空')
            if language is None or len(language) == 0:
                raise BadRequest(detail='Checker 语言不能为空')
            upload_custom_checker(problem=problem, code=code, language=language)
        else:
            problem.problem_info.problem_judge.checker = checker_type
            problem.problem_info.problem_judge.save()
        problem.make_update()
        return make_response()


@api_view()
@permission_classes([HasPolygonPermission])
def get_polygon_problem(request: Request, problem_id: int):
    """
    查看自己创建的题目, 公开的题目, 或者被授予阅读权限的题目
    """
    problem = Problem.objects.filter_user_public(problemrepository=get_main_problem_repo(),
                                                 display_id=problem_id,
                                                 user=request.user,
                                                 permission=ProblemPermissions.ReadProblem).first()
    return make_response(problem=FullProblemSerializer(problem).get_or_raise())


@api_view()
@permission_classes([HasPolygonPermission])
def export_polygon_problem_zip(request: Request, problem_id: int):
    """
    导出题目 zip
    """
    problem = Problem.objects.filter_user_public(problemrepository=get_main_problem_repo(),
                                                 display_id=problem_id,
                                                 user=request.user,
                                                 permission=ProblemPermissions.Export).first()
    problem_directory = ProblemDirectory.make(problem)
    response = HttpResponse(problem_directory.generate_zip(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={problem.title}.zip'
    return response


@api_view()
@permission_classes([HasPolygonPermission])
def list_polygon_problems(request):
    """
    列出自己可见的题目
    """
    problems = Problem.objects.filter_user_public(problemrepository=get_main_problem_repo(),
                                                  user=request.user,
                                                  permission=ProblemPermissions.ReadProblem).order_by(
        '-updated').order_by('-display_id')
    return make_response(problems=PolygonProblemSerializer(problems, many=True).data)


@api_view(['POST'])
@permission_classes([HasPolygonPermission])
@throttle_classes([SubmitRateThrottle])
@func_validate_request(SubmitCodePayload)
def submit_polygon_problem(request: Request, problem_id: int):
    """
    向自己创建的题目，或者被授予提交权限的题目，提交代码
    """
    problem = Problem.objects.filter_user_permission(problemrepository=get_main_problem_repo(),
                                                     display_id=problem_id,
                                                     user=request.user,
                                                     permission=ProblemPermissions.Submit).first()
    if problem is None:
        raise NotFound('题目未找到')
    else:
        submission = submit_polygon_problem_code(user=request.user,
                                                 repo=get_main_problem_repo(),
                                                 problem=problem,
                                                 payload=request.data)
        return make_response(submission=FullSubmissionSerializer(submission).data)


@api_view(['POST'])
@permission_classes([HasPolygonPermission])
def rejudge_polygon_problem(request: Request, submission_id: int):
    """
    重测提交
    """
    view_subquery = Problem.objects.filter_user_permission(problemrepository=get_main_problem_repo(),
                                                           user=request.user,
                                                           permission=ProblemPermissions.ReadSubmission)
    submission = Submission.objects.filter(repository=get_main_problem_repo(),
                                           problem__in=Subquery(view_subquery.values('id')),
                                           id=submission_id).first()
    if submission is None:
        raise NotFound('提交未找到')
    else:
        submission = rejudge_polygon_problem_code(submission)
        return make_response(submission=FullPolygonSubmissionSerializer(submission).data)


@api_view()
@permission_classes([HasPolygonPermission])
def list_polygon_problem_submissions(request: Request, problem_id: int):
    """
    列出该题目的所有提交列表
    """
    problem = Problem.objects.filter_user_permission(problemrepository=get_main_problem_repo(),
                                                     display_id=problem_id,
                                                     user=request.user,
                                                     permission=ProblemPermissions.ReadSubmission).first()
    if problem is None:
        raise NotFound('题目未找到')
    else:
        submissions = Submission.objects.filter(repository=get_main_problem_repo(), problem=problem)
        return make_response(submissions=SubmissionSerializer(submissions, many=True).data)


@api_view()
@permission_classes([HasPolygonPermission])
def get_polygon_submission(request: Request, submission_id: int):
    """
    获取提交
    """
    view_subquery = Problem.objects.filter_user_permission(problemrepository=get_main_problem_repo(),
                                                           user=request.user,
                                                           permission=ProblemPermissions.ReadSubmission)
    submission = Submission.objects.filter(repository=get_main_problem_repo(),
                                           problem__in=Subquery(view_subquery.values('id')),
                                           id=submission_id).first()
    if submission is None:
        raise NotFound('提交未找到')
    else:
        return make_response(submission=FullPolygonSubmissionSerializer(submission).data)


@api_view()
@permission_classes([HasPolygonPermission])
def list_polygon_submissions(request: Request):
    """
    获取提交列表
    """
    view_subquery = Problem.objects.filter_user_permission(problemrepository=get_main_problem_repo(),
                                                           user=request.user,
                                                           permission=ProblemPermissions.ReadSubmission)
    submissions = Submission.objects.filter(repository=get_main_problem_repo(),
                                            problem__in=Subquery(view_subquery.values('id')))
    return make_response(submissions=SubmissionSerializer(submissions, many=True).data)


class PolygonPermission(APIView):
    """
    编辑题目权限
    """
    permission_classes = [HasPolygonPermission]

    @staticmethod
    def get_problem_or_raise(request: Request, problem_id: int):
        problem = Problem.objects.filter(problemrepository=get_main_problem_repo(),
                                         display_id=problem_id,
                                         owner=request.user).first()
        if problem is None:
            raise NotFound('题目未找到')
        else:
            return problem

    def get(self, request: Request, problem_id: int):
        problem = self.get_problem_or_raise(request, problem_id)
        user_permissions = Problem.objects.list_user_permissions(problem.id)
        group_permissions = Problem.objects.list_group_permissions(problem.id)
        return make_response(user_permissions=UserPermissionSerializer(user_permissions, many=True).data,
                             group_permissions=GroupPermissionSerializer(group_permissions, many=True).data)

    @class_validate_request(EditPermissionPayload)
    def post(self, request: Request, problem_id: int):
        problem = self.get_problem_or_raise(request, problem_id)
        if 'user_id' in request.data or 'username' in request.data:
            if 'user_id' in request.data:
                user = User.objects.get(id=request.data['user_id'])
            else:
                user = User.objects.get(username=request.data['username'])
            if user is None:
                raise NotFound(detail='用户未找到')
            if problem.owner == user:
                return make_response(user_id=user.id)

            grant = False
            revoke = False
            if 'grant' in request.data:
                Problem.objects.grant_user_permission(user=user,
                                                      permission=request.data['grant'],
                                                      content_id=problem.id)
                grant = True
            if 'revoke' in request.data:
                revoke = Problem.objects.revoke_user_permission(user=user,
                                                                permission=request.data['revoke'],
                                                                content_id=problem.id)
            return make_response(user_id=user.id, grant=grant, revoke=revoke)
        elif 'group_id' in request.data:
            group = Group.objects.get(id=request.data['group_id'])
            grant = False
            revoke = False
            if 'grant' in request.data:
                Problem.objects.grant_group_permission(group=group,
                                                       permission=request.data['grant'],
                                                       content_id=problem.id)
                grant = True
            if 'revoke' in request.data:
                revoke = Problem.objects.revoke_group_permission(group=group,
                                                                 permission=request.data['revoke'],
                                                                 content_id=problem.id)
            return make_response(group_id=group.id, grant=grant, revoke=revoke)
        else:
            return make_error_response(status=status.HTTP_400_BAD_REQUEST)
