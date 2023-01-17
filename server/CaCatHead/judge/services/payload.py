from CaCatHead.contest.models import ContestRegistration
from CaCatHead.submission.models import Submission, ContestSubmission


class JudgeSubmissionPayload:
    def __init__(self, **kwargs):
        pass

    @staticmethod
    def make(submission: Submission,
             contest_submission: ContestSubmission,
             registration: ContestRegistration):
        submission_id = submission.id if submission is not None else None
        contest_submission_id = contest_submission.id if contest_submission is not None else None
        registration_id = registration.id if registration is not None else None

        sub = submission if submission is not None else contest_submission
        problem = sub.problem

        return JudgeSubmissionPayload(
            submission_id=submission_id,
            contest_submission_id=contest_submission_id,
            registration_id=registration_id,
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
        return {}

    @staticmethod
    def to_object():
        return JudgeSubmissionPayload()


class JudgeResponsePayload:
    def __init__(self):
        pass

    def to_representation(self):
        return {}

    @staticmethod
    def to_object():
        return JudgeSubmissionPayload()
