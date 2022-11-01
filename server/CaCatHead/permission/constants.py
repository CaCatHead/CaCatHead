from enum import Enum, unique


@unique
class PostPermissions(Enum):
    """
    公告系统使用的权限字符串常量
    """
    Read = 'read'
    Edit = 'edit'


@unique
class ProblemRepositoryPermissions(Enum):
    """
    题库系统使用的权限字符串常量
    """
    ListProblems = 'list_problems'  # 列出所有题目
    ReadProblem = 'read_problem'  # 获取所有题目的题面
    ReadSubmission = 'read_submission'  # 获取所有人的提交
    Submit = 'submit'  # 提交代码
    AddProblem = 'add_problem'  # 向题库中添加题目
    EditProblem = 'edit_problem'  # 编辑题库中的题目
    DeleteProblem = 'delete_problem'  # 删除题库中的题目


@unique
class ProblemPermissions(Enum):
    """
    题目系统使用的权限字符串常量
    """
    ReadProblem = 'read_problem'
    ReadSubmission = 'read_submission'
    Submit = 'submit'
    Edit = 'edit'
