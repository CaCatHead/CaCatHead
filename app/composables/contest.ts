import type { Contest, User } from './types';

export const isContestEnd = (contest: Contest) => {
  const now = new Date();
  const end_time = new Date(contest.end_time);
  if (now.getTime() >= end_time.getTime()) {
    return true;
  } else {
    return false;
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

export function displyaIdToIndex(display_id: number) {
  return String.fromCharCode(65 + (display_id - OFFSET));
}
