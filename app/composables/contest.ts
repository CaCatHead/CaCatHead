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
