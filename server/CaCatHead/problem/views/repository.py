from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from CaCatHead.core.decorators import class_validate_request
from CaCatHead.permission.constants import ProblemRepositoryPermissions, ProblemPermissions
from CaCatHead.permission.serializers import UserPermissionSerializer, GroupPermissionSerializer
from CaCatHead.problem.models import ProblemRepository, Problem
from CaCatHead.problem.serializers import ProblemRepositorySerializer, ProblemSerializer, FullProblemSerializer, \
    EditPermissionPayload, ProblemContentSerializer
from CaCatHead.problem.views.services import MAIN_PROBLEM_REPOSITORY
from CaCatHead.problem.views.services import copy_repo_problem
from CaCatHead.problem.views.submit import submit_problem_code
from CaCatHead.submission.models import Submission
from CaCatHead.submission.serializers import FullSubmissionSerializer, SubmissionSerializer
from CaCatHead.user.serializers import UserSerializer
from CaCatHead.utils import make_response, make_error_response


# ----- 题库 -----
@api_view()
def list_repos(request):
    """
    列出所有题库
    """
    repos = ProblemRepository.objects.filter_user_public(user=request.user,
                                                         permission=ProblemRepositoryPermissions.ListProblems).filter(
        ~Q(id=MAIN_PROBLEM_REPOSITORY.id)).filter(is_contest=False)
    return make_response(repos=ProblemRepositorySerializer(repos, many=True).data)


def check_repo(request: Request, repo_id: int, permission: str):
    if permission in [ProblemRepositoryPermissions.ListProblems, ProblemRepositoryPermissions.Submit,
                      ProblemRepositoryPermissions.ListSubmissions]:
        repo = ProblemRepository.objects.filter_user_public(user=request.user,
                                                            id=repo_id,
                                                            permission=permission).filter(is_contest=False).first()
    else:
        repo = ProblemRepository.objects.filter_user_permission(user=request.user,
                                                                id=repo_id,
                                                                permission=permission).filter(is_contest=False).first()
    if repo is None:
        raise NotFound(detail='题库未找到')
    elif repo == MAIN_PROBLEM_REPOSITORY:
        raise NotFound(detail='主题库不允许直接使用')
    else:
        return repo


def check_repo_problem(request: Request, repo_id: int, problem_display_id: int, repo_permission: str,
                       problem_permission: str):
    repo = check_repo(request, repo_id, repo_permission)
    if problem_permission in [ProblemPermissions.ReadProblem, ProblemPermissions.Submit]:
        problem = Problem.objects.filter_user_public(user=request.user,
                                                     problemrepository=repo,
                                                     display_id=problem_display_id,
                                                     permission=problem_permission).first()
    else:
        problem = Problem.objects.filter_user_permission(user=request.user,
                                                         problemrepository=repo,
                                                         display_id=problem_display_id,
                                                         permission=problem_permission).first()
    if problem is None:
        raise NotFound(detail='题目未找到')
    else:
        return repo, problem


@api_view()
def get_repo_info(request: Request, repo_id: int):
    repo = check_repo(request, repo_id, ProblemRepositoryPermissions.ListProblems)
    return make_response(repo=ProblemRepositorySerializer(repo).data)


@api_view()
def list_repo_problems(request: Request, repo_id: int):
    """
    列出题库中的所有题目
    """
    repo = check_repo(request, repo_id, ProblemRepositoryPermissions.ListProblems)
    problems = Problem.objects.filter_user_public(user=request.user,
                                                  problemrepository=repo,
                                                  permission=ProblemPermissions.ReadProblem)
    return make_response(repo=ProblemRepositorySerializer(repo).data,
                         problems=ProblemSerializer(problems, many=True).data)


@api_view()
def get_repo_problem_content(request: Request, repo_id: int, problem_id: int):
    """
    获取题库中的题目内容
    """
    repo, problem = check_repo_problem(request, repo_id, problem_id,
                                       ProblemRepositoryPermissions.ListProblems,
                                       ProblemPermissions.ReadProblem)
    return make_response(problem=ProblemContentSerializer(problem).get_or_raise())


class RepoPermission(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, repo_id: int):
        repo = ProblemRepository.objects.filter(id=repo_id, owner=request.user)
        if repo is None:
            raise NotFound('题库未找到')
        else:
            user_permissions = ProblemRepository.objects.list_user_permissions(repo.id)
            group_permissions = ProblemRepository.objects.list_group_permissions(repo.id)
            return make_response(user_permissions=UserPermissionSerializer(user_permissions, many=True).data,
                                 group_permissions=GroupPermissionSerializer(group_permissions, many=True).data)

    @class_validate_request(EditPermissionPayload)
    def post(self, request: Request, repo_id: int):
        """
        题库授权, 只有所有者能进行权限变动
        """
        repo = ProblemRepository.objects.filter(id=repo_id, owner=request.user)
        if repo is None:
            raise NotFound('题库未找到')
        else:
            if 'user_id' in request.data:
                user = User.objects.get(id=request.data['user_id'])
                user_data = UserSerializer(user).data
                if 'grant' in request.data:
                    grant = ProblemRepository.objects.grant_user_permission(user=user,
                                                                            permission=request.data['grant'],
                                                                            content_id=repo.id)
                    return make_response(user=user_data, grant=UserPermissionSerializer(grant))
                elif 'revoke' in request.data:
                    revoke = ProblemRepository.objects.revoke_user_permission(user=user,
                                                                              permission=request.data['revoke'],
                                                                              content_id=repo.id)
                    return make_response(user=user_data, revoke=revoke)
                else:
                    return make_response(user=user_data)
            elif 'group_id' in request.data:
                group = Group.objects.get(id=request.data['group_id'])
                if 'grant' in request.data:
                    grant = ProblemRepository.objects.grant_group_permission(group=group,
                                                                             permission=request.data['grant'],
                                                                             content_id=repo.id)
                    return make_response(group_id=group.id, grant=GroupPermissionSerializer(grant))
                elif 'revoke' in request.data:
                    revoke = ProblemRepository.objects.revoke_group_permission(group=group,
                                                                               permission=request.data['revoke'],
                                                                               content_id=repo.id)
                    return make_response(group_id=group.id, revoke=revoke)
                else:
                    return make_response(group_id=group.id)
            else:
                return make_error_response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_repo_problem(request: Request, repo_id: int, problem_id: int):
    """
    从主题库添加一个题目到当前题库
    """
    repo = check_repo(request, repo_id, ProblemRepositoryPermissions.AddProblem)
    problem = Problem.objects.filter_user_permission(user=request.user,
                                                     problemrepository=MAIN_PROBLEM_REPOSITORY,
                                                     id=problem_id,
                                                     permission=ProblemPermissions.Copy).first()
    if problem is None:
        return make_error_response(status=status.HTTP_400_BAD_REQUEST)
    else:
        new_problem = copy_repo_problem(request.user, repo, problem)
        return make_response(problem=FullProblemSerializer(new_problem).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_repo_problem(request: Request, repo_id: int, problem_id: int):
    """
    从当前题库中删除编号为 display_id 的题目
    """
    repo = check_repo(request, repo_id, ProblemRepositoryPermissions.DeleteProblem)
    problem = Problem.objects.filter(problemrepository=repo, display_id=problem_id).first()
    if problem is None:
        return make_error_response(status=status.HTTP_400_BAD_REQUEST)
    else:
        problem.delete()
        return make_response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_repo_problem(request: Request, repo_id: int, problem_id: int):
    """
    更新当前题库中的题目信息
    """
    repo = check_repo(request, repo_id, ProblemRepositoryPermissions.EditProblem)
    problem = Problem.objects.filter(problemrepository=repo, display_id=problem_id).first()
    if problem is None:
        return make_error_response(status=status.HTTP_400_BAD_REQUEST)
    else:
        if 'is_public' in request.data and isinstance(request.data['is_public'], bool):
            problem.is_public = request.data['is_public']
        problem.save()
        return make_response(problem=FullProblemSerializer(problem).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_repo_problem_code(request: Request, repo_id: int, problem_id: int):
    """
    提交代码
    """
    repo, problem = check_repo_problem(request, repo_id, problem_id,
                                       ProblemRepositoryPermissions.Submit,
                                       ProblemPermissions.Submit)
    submission = submit_problem_code(user=request.user,
                                     repo=repo,
                                     problem=problem,
                                     payload=request.data)
    return make_response(submission=FullSubmissionSerializer(submission).data)


@api_view()
def list_repo_submissions(request: Request, repo_id: int):
    repo = check_repo(request, repo_id, ProblemRepositoryPermissions.ListSubmissions)
    submissions = Submission.objects.filter(repository=repo).all()
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 30))
    paginator = Paginator(submissions, page_size)
    return make_response(count=paginator.count, page=page, page_size=page_size, num_pages=paginator.num_pages,
                         submissions=SubmissionSerializer(paginator.page(page).object_list, many=True).data)


@api_view()
def get_repo_submission(request: Request, repo_id: int, submission_id: int):
    repo = check_repo(request, repo_id, ProblemRepositoryPermissions.ReadSubmission)
    submission = Submission.objects.filter(repository=repo, id=submission_id).first()
    return make_response(submission=FullSubmissionSerializer(submission).data)
