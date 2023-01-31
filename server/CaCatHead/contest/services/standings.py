from CaCatHead.contest.models import ContestRegistration, ContestType
from CaCatHead.core.constants import Verdict
from CaCatHead.submission.models import ContestSubmission, ContestSubmissionType


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
    penalty = dict()
    penalty_unit = 20 * 60  # 单次罚时：20 分钟
    for sub in submissions:
        if sub.verdict == Verdict.Accepted:
            # 第一次通过
            if sub.problem.id not in accepted:
                accepted.add(sub.problem.id)
                score += 1
                dirty += sub.relative_time
                if sub.problem.id in penalty:
                    dirty += penalty[sub.problem.id] * penalty_unit
        elif sub.verdict in [Verdict.WrongAnswer, Verdict.TimeLimitExceeded, Verdict.IdlenessLimitExceeded,
                             Verdict.MemoryLimitExceeded, Verdict.OutputLimitExceeded, Verdict.RuntimeError]:
            skip_wrong = False
            try:
                # WA1 不计入罚时
                if 'results' in sub.detail and isinstance(sub.detail['results'], list):
                    if len(sub.detail['results']) == 1 and sub.detail['results']['sample']:
                        skip_wrong = True
            except Exception:
                pass
            if not skip_wrong:
                # 添加罚时次数
                if sub.problem.id not in penalty:
                    penalty[sub.problem.id] = 1
                else:
                    penalty[sub.problem.id] += 1

        # 只有 AC 或者错误提交，才会记录到排行榜的提交中
        if sub.verdict in [Verdict.Accepted, Verdict.WrongAnswer, Verdict.TimeLimitExceeded,
                           Verdict.IdlenessLimitExceeded,
                           Verdict.MemoryLimitExceeded, Verdict.OutputLimitExceeded, Verdict.RuntimeError]:
            # 压缩榜单需要记录的信息
            standings.append({
                'i': sub.id,
                'p': sub.problem.display_id,
                'v': sub.verdict,
                'c': sub.created.isoformat(),
                'r': sub.relative_time
            })

    registration.score = score
    registration.dirty = dirty
    registration.standings = {'submissions': standings, 'penalty': penalty}


def refresh_registration_standing(registration: ContestRegistration):
    registration.is_participate = True
    contest = registration.contest
    if contest.type == ContestType.icpc:
        refresh_icpc_standing(registration)
    elif contest.type == ContestType.ioi:
        pass
    registration.save()
