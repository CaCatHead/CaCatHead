from enum import Enum, unique


@unique
class PostPermissions(str, Enum):
    """
    公告系统使用的权限字符串常量
    """
    Read = 'read'
    Edit = 'edit'


@unique
class ProblemRepositoryPermissions(str, Enum):
    """
    题库系统使用的权限字符串常量
    """
    ListProblems = 'list_problems'  # 列出所有题目
    ReadSubmission = 'read_submission'  # 获取所有人的提交
    Submit = 'submit'  # 提交代码
    AddProblem = 'add_problem'  # 向题库中添加题目
    EditProblem = 'edit_problem'  # 编辑题库中的题目
    DeleteProblem = 'delete_problem'  # 删除题库中的题目


@unique
class ProblemPermissions(str, Enum):
    """
    题目系统使用的权限字符串常量
    """
    ReadProblem = 'read_problem'
    ReadSubmission = 'read_submission'
    Submit = 'submit'
    Edit = 'edit'
    Copy = 'copy'  # 将该题目从主题库复制到其他题库


@unique
class ContestPermissions(str, Enum):
    """
    比赛系统使用的权限字符串常量
    """
    ReadContest = 'read_contest'
    EditContest = 'edit_contest'
    RegisterContest = 'register_contest'
