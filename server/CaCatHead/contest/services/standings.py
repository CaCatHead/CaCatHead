from CaCatHead.contest.models import ContestRegistration, ContestType, Contest
from CaCatHead.core.constants import Verdict
from CaCatHead.submission.models import ContestSubmission, ContestSubmissionType


def is_submission_accepted(submission: ContestSubmission):
    return submission.verdict == Verdict.Accepted


def is_submission_wrong(submission: ContestSubmission):
    return submission.verdict in [Verdict.WrongAnswer, Verdict.TimeLimitExceeded, Verdict.IdlenessLimitExceeded,
                                  Verdict.MemoryLimitExceeded, Verdict.OutputLimitExceeded, Verdict.RuntimeError]


def is_submission_concerned(submission: ContestSubmission):
    """
    只有 AC 或者错误提交，才会记录到排行榜的提交中
    """
    return submission.verdict in [Verdict.Accepted, Verdict.WrongAnswer, Verdict.TimeLimitExceeded,
                                  Verdict.IdlenessLimitExceeded,
                                  Verdict.MemoryLimitExceeded, Verdict.OutputLimitExceeded, Verdict.RuntimeError]


def extract_submission(submission: ContestSubmission):
    """
    压缩榜单需要记录的信息
    """
    return {
        'i': submission.id,
        'p': submission.problem.display_id,
        'v': submission.verdict,
        'c': submission.created.isoformat(),
        'r': submission.relative_time
    }


def refresh_icpc_standing(registration: ContestRegistration):
    contest = registration.contest
    submissions = ContestSubmission.objects.filter(repository=contest.problem_repository,
                                                   owner=registration.team,
                                                   type=ContestSubmissionType.contestant
                                                   ).order_by('relative_time', 'judged').all()
    score = 0  # 通过题数
    dirty = 0  # 罚时，单位：秒
    standings = []
    accepted = set()
    scores = dict()  # 每个题目的得分
    penalty = dict()
    penalty_unit = 20 * 60  # 单次罚时：20 分钟
    for sub in submissions:
        pid = sub.problem.display_id
        if is_submission_accepted(sub):
            # 第一次通过
            if pid not in accepted:
                accepted.add(pid)
                score += 1
                dirty += sub.relative_time
                if pid in penalty:
                    dirty += penalty[pid] * penalty_unit
                else:
                    penalty[pid] = 0
        elif is_submission_wrong(sub):
            skip_wrong = False
            try:
                # WA1 不计入罚时
                if 'results' in sub.detail and isinstance(sub.detail['results'], list):
                    if len(sub.detail['results']) == 1 and sub.detail['results'][0]['sample']:
                        skip_wrong = True
            except Exception:
                pass
            if not skip_wrong:
                # 添加罚时次数
                if pid not in penalty:
                    penalty[pid] = 1
                else:
                    penalty[pid] += 1

        # 记录每个题的最高得分
        if pid not in scores:
            scores[pid] = sub.score
        else:
            scores[pid] = max(sub.score, scores[pid])

        # 只有 AC 或者错误提交，才会记录到排行榜的提交中
        if is_submission_concerned(sub):
            # 压缩榜单需要记录的信息
            standings.append(extract_submission(sub))

    registration.score = score
    registration.dirty = dirty
    registration.standings = {'submissions': standings, 'scores': scores, 'penalty': penalty}


def refresh_ioi_standing(registration: ContestRegistration):
    contest = registration.contest
    submissions = ContestSubmission.objects.filter(repository=contest.problem_repository,
                                                   owner=registration.team,
                                                   type=ContestSubmissionType.contestant
                                                   ).order_by('relative_time', 'judged').all()
    score = 0  # 通过题数
    dirty = 0  # 罚时，单位：秒
    accepted = set()  # 通过的题目编号
    scores = dict()  # 每个题目的得分
    penalty = dict()  # 每个题目的最高分提交时间数量
    standings = []  # 所有提交
    for sub in submissions:
        pid = sub.problem.display_id
        if is_submission_accepted(sub):
            if pid not in accepted:
                accepted.add(pid)
                penalty[pid] = sub.relative_time
        elif is_submission_wrong(sub):
            pass

        # 记录每个题的最高得分
        if pid not in scores:
            scores[pid] = sub.score
            penalty[pid] = sub.relative_time
        elif sub.score > scores[pid]:
            scores[pid] = sub.score
            penalty[pid] = sub.relative_time

        # 只有 AC 或者错误提交，才会记录到排行榜的提交中
        if is_submission_concerned(sub):
            # 压缩榜单需要记录的信息
            standings.append(extract_submission(sub))

    for _, value in scores.items():
        score += value
    for _, value in scores.items():
        dirty += value
    registration.score = score
    registration.dirty = dirty
    registration.standings = {'submissions': standings, 'scores': scores, 'penalty': penalty}


def refresh_registration_standing(registration: ContestRegistration):
    registration.is_participate = True
    contest = registration.contest
    if contest.type == ContestType.icpc:
        refresh_icpc_standing(registration)
    elif contest.type == ContestType.ioi:
        refresh_ioi_standing(registration)
    registration.save()


def export_standings(contest: Contest, registrations: list[ContestRegistration]):
    problems = contest.problem_repository.problems.all()
    problem_count = len(problems)

    def get_row(r: [int, ContestRegistration]):
        index = r[0]
        registration = r[1]
        detail = []
        for problem in problems:
            pid = problem.display_id
            standings = registration.standings
            print(standings)
            if 'scores' in standings and pid in standings['scores']:
                s = standings['scores'][pid]
                detail.append(str(s))
            else:
                detail.append('')
        return f'{index + 1},{registration.team.name},{registration.score},{registration.dirty},{",".join(detail)}'

    header = '排名,姓名,分数,罚时,' + ','.join(map(lambda x: chr(65 + x), range(problem_count)))
    body = map(get_row, enumerate(registrations))
    return header + '\n' + '\n'.join(body)
