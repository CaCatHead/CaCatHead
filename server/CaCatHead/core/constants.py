from enum import unique, Enum

NJUST_ICPC_GROUP = 'njust_icpc_group'

GENERAL_USER_GROUP = 'general_user_group'

MAIN_PROBLEM_REPOSITORY = '主题库'


@unique
class Permissions(str, Enum):
    """
    全局权限字符串常量
    """
    POLYGON = 'problem.polygon'


@unique
class Verdict(str, Enum):
    Waiting = 'Waiting'
    Running = 'Running'
    Compiling = 'Compiling'
    Accepted = 'Accepted'
    WrongAnswer = 'WrongAnswer'
    TimeLimitExceeded = 'TimeLimitExceeded'
    IdlenessLimitExceeded = 'IdlenessLimitExceeded'
    MemoryLimitExceeded = 'MemoryLimitExceeded'
    OutputLimitExceeded = 'OutputLimitExceeded'
    RuntimeError = 'RuntimeError'
    Point = 'Point'
    PartiallyCorrect = 'PartiallyCorrect'
    CompileError = 'CompileError'
    SystemError = 'SystemError'
    JudgeError = 'JudgeError'
    TestCaseError = 'TestCaseError'

    @classmethod
    def parse(cls, text: str):
        text = text.replace(' ', '')  # Remove space , i.e. Compile Error -> CompileError
        if text == 'CompileError':
            return Verdict.CompileError
        elif text == 'TimeLimitExceeded':
            return Verdict.TimeLimitExceeded
        elif text == 'MemoryLimitExceeded':
            return Verdict.MemoryLimitExceeded
        elif text == 'OutputLimitExceeded':
            return Verdict.OutputLimitExceeded
        elif text == 'RuntimeError':
            return Verdict.RuntimeError
        elif text == 'WrongAnswer':
            return Verdict.WrongAnswer
        elif text == 'Accepted':
            return Verdict.Accepted
        else:
            return Verdict.SystemError
