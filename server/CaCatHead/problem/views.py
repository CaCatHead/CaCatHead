from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.exceptions import NotFound
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request

from CaCatHead.core.decorators import HasPolygonPermission, func_validate_request
from CaCatHead.permission.constants import ProblemRepositoryPermissions, ProblemPermissions
from CaCatHead.problem.models import ProblemRepository, Problem
from CaCatHead.problem.serializers import ProblemRepositorySerializer, ProblemSerializer, CreateProblemPayload, \
    EditProblemPayload, FullProblemSerializer
from CaCatHead.problem.services import make_problem, edit_problem, MAIN_PROBLEM_REPOSITORY, make_problem_by_uploading
from CaCatHead.problem.submit import submit_problem_code
from CaCatHead.submission.models import Submission
from CaCatHead.submission.serializers import FullSubmissionSerializer, SubmissionSerializer
from CaCatHead.utils import make_response


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
    return make_response(problem=ProblemSerializer(problem).data)


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
@func_validate_request(EditProblemPayload)
def edit_created_problem(request: Request, problem_id: int):
    """
    编辑自己创建的题目, 或者被授予编辑权限的题目
    """
    problem = Problem.objects.filter_user_permission(problemrepository=MAIN_PROBLEM_REPOSITORY,
                                                     id=problem_id,
                                                     user=request.user,
                                                     permission=ProblemPermissions.Edit).first()
    if problem is None:
        raise NotFound('题目未找到')
    else:
        problem = edit_problem(problem=problem, payload=request.data)
        return make_response(problem=FullProblemSerializer(problem).get_or_raise())


@api_view()
@permission_classes([HasPolygonPermission])
def get_created_problems(request: Request, problem_id: int):
    """
    查看自己创建的题目, 公开的题目, 或者被授予阅读权限的题目
    """
    problem = Problem.objects.filter_user_public(problemrepository=MAIN_PROBLEM_REPOSITORY,
                                                 id=problem_id,
                                                 user=request.user,
                                                 permission=ProblemPermissions.ReadProblem).first()
    return make_response(problem=FullProblemSerializer(problem).get_or_raise())


@api_view()
@permission_classes([HasPolygonPermission])
def list_created_problems(request):
    """
    列出自己可见的题目
    """
    problems = Problem.objects.filter_user_public(problemrepository=MAIN_PROBLEM_REPOSITORY,
                                                  user=request.user,
                                                  permission=ProblemPermissions.ReadProblem)
    return make_response(problems=ProblemSerializer(problems, many=True).data)


@api_view(['POST'])
@permission_classes([HasPolygonPermission])
def submit_created_problem(request: Request, problem_id: int):
    """
    向自己创建的题目，或者被授予提交权限的题目，提交代码
    """
    problem = Problem.objects.filter_user_permission(problemrepository=MAIN_PROBLEM_REPOSITORY,
                                                     id=problem_id,
                                                     user=request.user,
                                                     permission=ProblemPermissions.Submit).first()
    if problem is None:
        raise NotFound('题目未找到')
    else:
        submission = submit_problem_code(user=request.user,
                                         repo=MAIN_PROBLEM_REPOSITORY,
                                         problem=problem,
                                         payload=request.data)
        return make_response(submission=FullSubmissionSerializer(submission).data)


@api_view()
@permission_classes([HasPolygonPermission])
def get_created_problem_submission(request: Request, submission_id: int):
    """
    获取提交
    """
    submission = Submission.objects.filter(repository=MAIN_PROBLEM_REPOSITORY,
                                           owner=request.user,
                                           id=submission_id).first()
    if submission is None:
        raise NotFound('提交未找到')
    else:
        return make_response(submission=FullSubmissionSerializer(submission).data)


@api_view()
@permission_classes([HasPolygonPermission])
def list_created_problem_submissions(request: Request):
    """
    获取提交
    """
    submissions = Submission.objects.filter(repository=MAIN_PROBLEM_REPOSITORY,
                                            owner=request.user)
    return make_response(submissions=SubmissionSerializer(submissions, many=True).data)


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
    repo = ProblemRepository.objects.filter_user_public(user=request.user, id=repo_id,
                                                        permission=ProblemRepositoryPermissions.ListProblems).first()
    if repo is None:
        raise NotFound(detail='题库未找到')
    else:
        problems = Problem.objects.filter(problemrepository=repo)
        return make_response(problems=ProblemSerializer(problems, many=True).data)
