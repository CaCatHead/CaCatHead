from enum import unique, Enum

NJUST_ICPC_GROUP = 'njust_icpc_group'

MAIN_PROBLEM_REPOSITORY = '主题库'


@unique
class Permissions(Enum):
    """
    全局权限字符串常量
    """
    POLYGON = 'problem.polygon'
