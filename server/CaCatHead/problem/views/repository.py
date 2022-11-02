from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from CaCatHead.permission.constants import ProblemRepositoryPermissions, ProblemPermissions
from CaCatHead.problem.models import ProblemRepository, Problem
from CaCatHead.problem.serializers import ProblemRepositorySerializer, ProblemSerializer, FullProblemSerializer
from CaCatHead.problem.services import MAIN_PROBLEM_REPOSITORY
from CaCatHead.problem.submit import submit_problem_code
from CaCatHead.submission.serializers import FullSubmissionSerializer
from CaCatHead.utils import make_response


# ----- 题库 -----
@api_view()
def list_repos(request):
    """
    列出所有题库
    """
    repos = ProblemRepository.objects.filter_user_public(user=request.user,
                                                         permission=ProblemRepositoryPermissions.ListProblems)
    return make_response(repos=ProblemRepositorySerializer(repos, many=True).data)


def check_repo(request: Request, repo_id: int, permission: str):
    if permission == ProblemRepositoryPermissions.ListProblems:
        repo = ProblemRepository.objects.filter_user_public(user=request.user,
                                                            id=repo_id,
                                                            permission=permission).first()
    else:
        repo = ProblemRepository.objects.filter_user_permission(user=request.user,
                                                                id=repo_id,
                                                                permission=permission).first()
    if repo is None:
        raise NotFound(detail='题库未找到')
    elif repo == MAIN_PROBLEM_REPOSITORY:
        raise NotFound(detail='主题库不允许直接使用')
    else:
        return repo


def check_repo_problem(request: Request, repo_id: int, problem_id: int, repo_permission: str, problem_permission: str):
    repo = check_repo(request, repo_id, repo_permission)
    if problem_permission in [ProblemPermissions.ReadProblem, ProblemPermissions.Submit]:
        problem = Problem.objects.filter_user_public(user=request.user,
                                                     problemrepository=repo,
                                                     id=problem_id,
                                                     permission=problem_permission)
    else:
        problem = Problem.objects.filter_user_permission(user=request.user,
                                                         problemrepository=repo,
                                                         id=problem_id,
                                                         permission=problem_permission)
    if problem is None:
        raise NotFound(detail='题目未找到')
    else:
        return repo, problem


@api_view()
def list_repo_problems(request: Request, repo_id: int):
    """
    列出题库中的所有题目
    """
    repo = check_repo(request, repo_id, ProblemRepositoryPermissions.ListProblems)
    problems = Problem.objects.filter_user_public(user=request.user,
                                                  problemrepository=repo,
                                                  permission=ProblemPermissions.ReadProblem)
    return make_response(problems=ProblemSerializer(problems, many=True).data)


@api_view()
def get_repo_problem_content(request: Request, repo_id: int, problem_id: int):
    """
    获取题库中的题目内容
    """
    repo, problem = check_repo_problem(request, repo_id, problem_id,
                                       ProblemRepositoryPermissions.ListProblems,
                                       ProblemPermissions.ReadProblem)
    return make_response(problem=FullProblemSerializer(problem).get_or_raise())


@api_view(['POST'])
def submit_repo_problem_content(request: Request, repo_id: int, problem_id: int):
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
