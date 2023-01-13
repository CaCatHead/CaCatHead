from django.utils import timezone

from CaCatHead.core.constants import Verdict
from CaCatHead.submission.models import ContestSubmission, Submission


def can_rejudge_submission(submission: Submission | ContestSubmission):
    if submission.verdict in [Verdict.Waiting]:
        delta = timezone.now() - submission.created
        return delta.total_seconds() >= 60
    elif submission.verdict in [Verdict.Compiling, Verdict.Running]:
        delta = timezone.now() - submission.judged
        return delta.total_seconds() >= 60
    else:
        return True
