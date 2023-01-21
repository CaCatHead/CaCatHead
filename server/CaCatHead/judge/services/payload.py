from CaCatHead.contest.models import ContestRegistration
from CaCatHead.submission.models import Submission, ContestSubmission


class JudgeSubmissionPayload:
    def __init__(self,
                 submission_id,
                 contest_submission_id,
                 registration_id,
                 owner_id,
                 code, language,
                 problem_id, problem_judge_id, problem_type,
                 time_limit, memory_limit,
                 checker, custom_checker_id,
                 testcase_version: int, testcase_detail: dict,
                 judge_extra_info: dict):
        self.submission_id = submission_id
        self.contest_submission_id = contest_submission_id
        self.registration_id = registration_id
        self.owner_id = owner_id
        self.code = code
        self.language = language
        self.problem_id = problem_id
        self.problem_judge_id = problem_judge_id
        self.problem_type = problem_type
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.checker = checker
        self.custom_checker_id = custom_checker_id
        self.testcase_version = testcase_version
        self.testcase_detail = testcase_detail
        self.judge_extra_info = judge_extra_info

    @staticmethod
    def make(submission: Submission = None,
             contest_submission: ContestSubmission = None,
             registration: ContestRegistration = None):
        submission_id = submission.id if submission is not None else None
        contest_submission_id = contest_submission.id if contest_submission is not None else None
        registration_id = registration.id if registration is not None else None
        owner_id = submission.owner_id if submission is not None else contest_submission.owner_id

        sub = submission if submission is not None else contest_submission
        problem = sub.problem

        return JudgeSubmissionPayload(
            submission_id=submission_id,
            contest_submission_id=contest_submission_id,
            registration_id=registration_id,
            owner_id=owner_id,
            code=sub.code,
            language=sub.language,
            problem_id=problem.id,
            problem_judge_id=problem.problem_info.problem_judge_id,
            problem_type=problem.problem_type,
            time_limit=problem.time_limit,
            memory_limit=problem.memory_limit,
            checker=problem.problem_info.problem_judge.checker,
            custom_checker_id=problem.problem_info.problem_judge.custom_checker_id,
            testcase_version=problem.problem_info.problem_judge.testcase_version,
            testcase_detail=problem.problem_info.problem_judge.testcase_detail,
            judge_extra_info=problem.problem_info.problem_judge.extra_info
        )

    def to_representation(self):
        return {
            'sid': self.submission_id,
            'csid': self.contest_submission_id,
            'rid': self.registration_id,
            'oid': self.owner_id,
            'c': self.code,
            'l': self.language,
            'pid': self.problem_id,
            'pjid': self.problem_judge_id,
            'pt': self.problem_type,
            'tl': self.time_limit,
            'ml': self.memory_limit,
            'chk': self.checker,
            'chkid': self.custom_checker_id,
            'tv': self.testcase_version,
            'td': self.testcase_detail,
            'info': self.judge_extra_info
        }

    @staticmethod
    def to_object(obj: dict):
        return JudgeSubmissionPayload(
            submission_id=obj['sid'],
            contest_submission_id=obj['csid'],
            registration_id=obj['rid'],
            owner_id=obj['oid'],
            code=obj['c'],
            language=obj['l'],
            problem_id=obj['pid'],
            problem_judge_id=obj['pjid'],
            problem_type=obj['pt'],
            time_limit=obj['tl'],
            memory_limit=obj['ml'],
            checker=obj['chk'],
            custom_checker_id=obj['chkid'],
            testcase_version=obj['tv'],
            testcase_detail=obj['td'],
            judge_extra_info=obj['info']
        )


class JudgeResponsePayload:
    def __init__(self):
        pass

    def to_representation(self):
        return {}

    @staticmethod
    def to_object():
        return JudgeSubmissionPayload()
