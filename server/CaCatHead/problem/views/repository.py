from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from CaCatHead.permission.constants import ProblemRepositoryPermissions
from CaCatHead.problem.models import ProblemRepository, Problem
from CaCatHead.problem.serializers import ProblemRepositorySerializer, ProblemSerializer
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


@api_view
def list_repo_problems(request, repo_id: int):
    """
    列出题库中的所有题目
    """
    repo = ProblemRepository.objects.filter_user_public(user=request.user,
                                                        id=repo_id,
                                                        permission=ProblemRepositoryPermissions.ListProblems).first()
    if repo is None:
        raise NotFound(detail='题库未找到')
    else:
        problems = Problem.objects.filter(problemrepository=repo)
        return make_response(problems=ProblemSerializer(problems, many=True).data)
