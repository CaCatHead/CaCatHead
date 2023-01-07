import type { Contest, User } from './types';

import { formatInterval } from './date';

export const useContestLastProblem = (id: string | string[]) =>
  useLocalStorage(`contest/${id}/last-problem`, 1000);

export const isContestStart = (contest: Contest) => {
  const now = new Date();
  const start_time = new Date(contest.start_time);
  if (now.getTime() >= start_time.getTime()) {
    return true;
  } else {
    return false;
  }
};

export const isContestEnd = (contest: Contest) => {
  const now = new Date();
  const end_time = new Date(contest.end_time);
  if (now.getTime() >= end_time.getTime()) {
    return true;
  } else {
    return false;
  }
};

export const getContestDuration = (contest: Contest) => {
  const d = formatInterval(
    new Date(contest.start_time),
    new Date(contest.end_time)
  );
  const h = d.hours ?? 0;
  const m = d.minutes ?? 0;
  return h * 60 + m;
};

export const formatContestDuration = (row: Contest) => {
  const d = formatInterval(new Date(row.start_time), new Date(row.end_time));
  const h = d.hours ? `${d.hours} 小时` : '';
  const m = d.minutes ? `${d.minutes} 分钟` : '';
  if (h && m) {
    return h + ' ' + m;
  } else {
    return h + m;
  }
};

export const isContestAdmin = (contest: Contest, user: User | undefined) => {
  return user && contest.owner.id === user.id;
};

export function indexToOffset(pid: string) {
  if (/^[A-Z]$/.test(pid)) {
    return pid.charCodeAt(0) - 65;
  } else if (/^[a-z]$/.test(pid)) {
    return pid.charCodeAt(0) - 97;
  } else {
    return undefined;
  }
}

const OFFSET = 1000;

export function indexToDisplayId(pid: string) {
  const v = indexToOffset(pid);
  if (v !== undefined) {
    return v + OFFSET;
  } else {
    return undefined;
  }
}

export function displyaIdToIndex(display_id: number) {
  return String.fromCharCode(65 + (display_id - OFFSET));
}
