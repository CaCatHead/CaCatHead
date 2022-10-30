from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound

from CaCatHead.core.decorators import HasPolygonPermission, func_validate_request
from CaCatHead.permission.constants import ProblemRepositoryPermissions
from CaCatHead.problem.models import ProblemRepository, Problem, MAIN_PROBLEM_REPOSITORY
from CaCatHead.problem.serializers import ProblemRepositorySerializer, ProblemSerializer, CreateProblemPayload
from CaCatHead.problem.services import make_problem
from CaCatHead.utils import make_response


# Polygon
@api_view(['POST'])
@permission_classes([HasPolygonPermission])
@func_validate_request(CreateProblemPayload)
def create_problem(request):
    """
    创建题目
    """
    title = request.data['title']
    display_id = request.data.get('display_id', None)
    problem = make_problem(title=title, user=request.user, display_id=display_id)
    return make_response(problem=ProblemSerializer(problem).data)


@api_view(['POST'])
@permission_classes([HasPolygonPermission])
def upload_problem(request):
    """
    上传题目
    """
    return make_response()


@api_view()
@permission_classes([HasPolygonPermission])
def edit_problem(request):
    """
    编辑题目
    """
    return make_response()


@api_view()
@permission_classes([HasPolygonPermission])
def get_created_problems(request, problem_id: int):
    """
    查看自己创建的题目
    """
    problem = Problem.objects.filter(problemrepository=MAIN_PROBLEM_REPOSITORY,
                                     id=problem_id,
                                     owner=request.user).first()
    return make_response(problem=ProblemSerializer(problem).get_or_raise())


@api_view()
@permission_classes([HasPolygonPermission])
def list_created_problems(request):
    """
    列出自己创建的题目
    """
    problems = Problem.objects.filter(problemrepository=MAIN_PROBLEM_REPOSITORY, owner=request.user)
    return make_response(problems=ProblemSerializer(problems, many=True).data)


# 题库
@api_view()
def list_repos(request):
    """
    列出所有题库
    """
    repos = ProblemRepository.objects.filter_user(user=request.user,
                                                  permission=ProblemRepositoryPermissions.ListProblems)
    return make_response(repos=ProblemRepositorySerializer(repos, many=True).data)


@api_view
def list_repo_problems(request, repo_id: int):
    """
    列出题库中的所有题目
    """
    repo = ProblemRepository.objects.filter_user(user=request.user, id=repo_id,
                                                 permission=ProblemRepositoryPermissions.ListProblems).first()
    if repo is None:
        raise NotFound(detail='题库未找到')
    else:
        problems = Problem.objects.filter(problemrepository=repo)
        return make_response(problems=ProblemSerializer(problems, many=True).data)
