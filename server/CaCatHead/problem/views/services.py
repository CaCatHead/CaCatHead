import logging

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone

from CaCatHead.core.constants import MAIN_PROBLEM_REPOSITORY as MAIN_PROBLEM_REPOSITORY_NAME
from CaCatHead.core.exceptions import BadRequest
from CaCatHead.problem.models import Problem, ProblemInfo, ProblemContent, ProblemJudge, \
    ProblemRepository, SourceCode, SourceCodeTypes, DefaultCheckers
from CaCatHead.problem.serializers import EditProblemPayload, TestcaseInfoPayload
from CaCatHead.problem.views.upload import upload_problem_arch, ProblemDirectory

logger = logging.getLogger(__name__)

DEFAULT_DISPLAY_ID = 1000

try:
    MAIN_PROBLEM_REPOSITORY = ProblemRepository.objects.get(name=MAIN_PROBLEM_REPOSITORY_NAME)
except Exception as ex:
    MAIN_PROBLEM_REPOSITORY = None


def get_main_problem_repo():
    global MAIN_PROBLEM_REPOSITORY
    if MAIN_PROBLEM_REPOSITORY is None:
        MAIN_PROBLEM_REPOSITORY = ProblemRepository.objects.get(name=MAIN_PROBLEM_REPOSITORY_NAME)
        return MAIN_PROBLEM_REPOSITORY
    else:
        return MAIN_PROBLEM_REPOSITORY


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

    main_repo = get_main_problem_repo()
    if display_id is None:
        display_id = main_repo.problems.aggregate(models.Max('display_id'))['display_id__max']
        if display_id is None:
            display_id = DEFAULT_DISPLAY_ID
        else:
            display_id += 1

    try:
        problem = Problem(repository=main_repo,
                          display_id=display_id,
                          title=title,
                          problem_info=problem_info,
                          owner=user,
                          is_public=False)
        problem.save()
        main_repo.problems.add(problem)
        return problem
    except Exception:
        problem_info.delete()
        problem_content.delete()
        problem_judge.delete()
        raise BadRequest(detail='创建题目失败')


def edit_problem(problem: Problem, payload: dict):
    if 'title' in payload:
        problem.title = payload['title']
        problem.problem_info.problem_content.title = payload['title']
    if 'problem_type' in payload:
        problem.problem_type = payload['problem_type']
        problem.problem_info.problem_judge.problem_type = payload['problem_type']
    if 'display_id' in payload:
        problem.display_id = payload['display_id']
    if 'time_limit' in payload:
        problem.time_limit = payload['time_limit']
        problem.problem_info.problem_judge.time_limit = payload['time_limit']
    if 'memory_limit' in payload:
        problem.memory_limit = payload['memory_limit']
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

    problem.updated = timezone.now()
    problem.save()
    problem.problem_info.problem_content.save()
    problem.problem_info.problem_judge.save()
    ProblemDirectory.make(problem).save_config(problem)

    return problem


def upload_custom_checker(problem: Problem, code: str, language: str):
    old_checker = problem.problem_info.problem_judge.custom_checker

    source = SourceCode(
        type=SourceCodeTypes.checker,
        code=code,
        code_length=len(code),
        language=language,
    )
    source.save()

    problem.problem_info.problem_judge.checker = DefaultCheckers.custom
    problem.problem_info.problem_judge.custom_checker = source
    problem.problem_info.problem_judge.save()

    if old_checker is not None:
        old_checker.delete()


def make_problem_by_uploading(zip_content: InMemoryUploadedFile, user: User):
    problem = make_problem('unknown', user=user)
    problem_directory = upload_problem_arch(problem, zip_content)

    def clear():
        # 上传的题目不合法, 删除该题目
        problem_info = problem.problem_info
        problem_content = problem_info.problem_content
        problem_judge = problem.problem_info.problem_judge
        problem.delete()
        problem_info.delete()
        problem_content.delete()
        problem_judge.delete()

    if problem_directory is None:
        clear()
        raise BadRequest(detail='题目压缩包上传失败')
    else:
        try:
            save_arch_to_database(problem, problem_directory)
            return problem
        except Exception as ex:
            clear()
            raise ex


def edit_problem_by_uploading(zip_content: InMemoryUploadedFile, problem: Problem):
    # 旧的测试用例版本号
    old_testcase_version = problem.problem_info.problem_judge.testcase_version
    # 更新测试用例版本号
    problem.problem_info.problem_judge.testcase_version = old_testcase_version + 1
    problem.problem_info.problem_judge.save()
    # 保存测试用例
    problem_directory = upload_problem_arch(problem, zip_content)

    if problem_directory is None:
        # 恢复测试用例版本号
        problem.problem_info.problem_judge.testcase_version = old_testcase_version
        problem.problem_info.problem_judge.save()
        raise BadRequest(detail='题目压缩包上传失败')
    else:
        # 将压缩包内的更新，写入到数据库
        save_arch_to_database(problem, problem_directory)
        # 将数据库中的信息，同步到题目目录
        problem_directory.save_config(problem)

    return problem


def save_arch_to_database(problem: Problem, problem_directory: ProblemDirectory):
    config_json = problem_directory.config
    if 'testcases' in config_json:
        testcases_config = config_json['testcases']
        # 检查测试用例格式是否合法
        valid = isinstance(testcases_config, list)
        if valid:
            for testcase in testcases_config:
                serializer = TestcaseInfoPayload(data=testcase)
                if not serializer.is_valid(raise_exception=False):
                    valid = False
        if valid:
            problem_judge = problem.problem_info.problem_judge
            problem_judge.score = 0
            problem_judge.testcase_count = len(testcases_config)
            problem_judge.testcase_detail = testcases_config
            for testcase in testcases_config:
                problem_judge.score += testcase['score']
            problem_judge.save()
        if not valid:
            raise BadRequest(detail='测试用例格式非法')
    if 'problem' in config_json:
        problem_config = config_json['problem']
        serializer = EditProblemPayload(data=problem_config)
        if serializer.is_valid():
            edit_problem(problem, problem_config)
        else:
            raise BadRequest(detail={'detail': serializer.errors})


def copy_repo_problem(user: User, repo: ProblemRepository, problem: Problem, display_id=None):
    """
    移动 Polygon Problem 到 repo
    """
    if display_id is None:
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
