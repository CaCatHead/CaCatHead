from enum import Enum, unique


@unique
class PostPermissions(Enum):
    """
    公告系统使用的权限字符串常量
    """
    Read = 'read'
    Write = 'write'
