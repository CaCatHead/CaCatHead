from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from rest_framework import status
from rest_framework.exceptions import APIException

from CaCatHead.core.constants import MAIN_PROBLEM_REPOSITORY as MAIN_PROBLEM_REPOSITORY_NAME
from CaCatHead.problem.models import Problem, ProblemInfo, ProblemContent, ProblemJudge, \
    ProblemRepository
from CaCatHead.problem.serializers import EditProblemPayload
from CaCatHead.problem.views.upload import upload_problem_zip

try:
    MAIN_PROBLEM_REPOSITORY = ProblemRepository.objects.get(name=MAIN_PROBLEM_REPOSITORY_NAME)
except Exception:
    MAIN_PROBLEM_REPOSITORY = None

DEFAULT_DISPLAY_ID = 1000


def make_problem(title: str, user: User, display_id=None):
    # init problem content
    problem_content = ProblemContent(title=title)
    problem_content.save()

    # init problem judge info
    problem_judge = ProblemJudge()
    problem_judge.save()

    # init problem info
    problem_info = ProblemInfo(problem_content=problem_content, problem_judge=problem_judge, owner=user)
    problem_info.save()

    if display_id is None:
        display_id = MAIN_PROBLEM_REPOSITORY.problems.aggregate(models.Max('display_id'))['display_id__max']
        if display_id is None:
            display_id = DEFAULT_DISPLAY_ID
        else:
            display_id += 1

    try:
        problem = Problem(repository=MAIN_PROBLEM_REPOSITORY,
                          display_id=display_id,
                          title=title,
                          problem_info=problem_info,
                          owner=user,
                          is_public=False)
        problem.save()
        MAIN_PROBLEM_REPOSITORY.problems.add(problem)
        return problem
    except Exception:
        problem_info.delete()
        problem_content.delete()
        problem_judge.delete()
        raise APIException(detail='创建题目失败', code=status.HTTP_400_BAD_REQUEST)


def edit_problem(problem: Problem, payload: dict):
    if 'title' in payload:
        problem.title = payload['title']
        problem.problem_info.problem_content.title = payload['title']
    if 'display_id' in payload:
        # TODO: check unique display_id
        problem.display_id = payload['display_id']
    if 'time_limit' in payload:
        problem.time_limit = payload['time_limit']
        problem.problem_info.problem_judge.time_limit = payload['time_limit']
    if 'memory_limit' in payload:
        problem.time_limit = payload['memory_limit']
        problem.problem_info.problem_judge.memory_limit = payload['memory_limit']
    if 'description' in payload:
        problem.problem_info.problem_content.description = payload['description']
    if 'input' in payload:
        problem.problem_info.problem_content.input = payload['input']
    if 'output' in payload:
        problem.problem_info.problem_content.output = payload['output']
    if 'sample' in payload:
        problem.problem_info.problem_content.sample = payload['sample']
    if 'hint' in payload:
        problem.problem_info.problem_content.hint = payload['hint']
    if 'source' in payload:
        problem.problem_info.problem_content.source = payload['source']
    if 'extra_content' in payload:
        problem.problem_info.problem_content.extra_content = payload['extra_content']
    if 'extra_judge' in payload:
        problem.problem_info.problem_judge.extra_info = payload['extra_judge']

    problem.save()
    problem.problem_info.problem_content.save()
    problem.problem_info.problem_judge.save()

    return problem


def make_problem_by_uploading(zip_content: InMemoryUploadedFile, user: User):
    problem = make_problem('unknown', user=user)
    config_json = upload_problem_zip(problem.id, zip_content)

    if config_json is not None:
        if 'problem' in config_json:
            problem_config = config_json['problem']
            serializer = EditProblemPayload(data=problem_config)
            if serializer.is_valid():
                edit_problem(problem, problem_config)
        if 'testcases' in config_json:
            # TODO: check testcases format valid
            testcases_config = config_json['testcases']
            problem_judge = problem.problem_info.problem_judge
            problem_judge.testcase_count = len(testcases_config)
            problem_judge.testcase_detail = testcases_config
            for testcase in testcases_config:
                problem_judge.score += testcase['score']
            problem_judge.save()
        return problem

    # 上传的题目不合法, 删除该题目
    problem_info = problem.problem_info
    problem_content = problem_info.problem_content
    problem_judge = problem.problem_info.problem_judge
    problem.delete()
    problem_info.delete()
    problem_content.delete()
    problem_judge.delete()

    return None


def copy_repo_problem(user: User, repo: ProblemRepository, problem: Problem):
    display_id = repo.problems.aggregate(models.Max('display_id'))['display_id__max']
    if display_id is None:
        display_id = DEFAULT_DISPLAY_ID
    else:
        display_id += 1

    new_problem = Problem(repository=repo,
                          display_id=display_id,
                          title=problem.title,
                          problem_type=problem.problem_type,
                          time_limit=problem.time_limit,
                          memory_limit=problem.memory_limit,
                          problem_info=problem.problem_info,
                          extra_info=problem.extra_info,
                          owner=user,
                          is_public=False)
    new_problem.save()
    repo.problems.add(new_problem)
    return new_problem
