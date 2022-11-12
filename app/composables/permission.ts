import type { User } from './types';

export interface UserPermission {
  user: User;
  content_type: string;
  content_id: number;
  codename: string;
}

export enum ProblemPermissions {
  ReadProblem = 'read_problem',
  ReadSubmission = 'read_submission',
  Submit = 'submit',
  Edit = 'edit',
  Copy = 'copy',
}

export function groupUserPermissions(
  permissions: UserPermission[],
  initPerm: Record<string, boolean> = {}
) {
  const map = new Map<number, string[]>();
  const users = new Map<number, User>();
  for (const permission of permissions) {
    if (!map.has(permission.user.id)) {
      map.set(permission.user.id, []);
      users.set(permission.user.id, permission.user);
    }
    map.get(permission.user.id)!.push(permission.codename);
  }
  const data = [];
  for (const [userId, perms] of map) {
    const d = {
      user: users.get(userId)!,
      permissions: { ...initPerm } as Record<string, boolean>,
    };
    for (const p of perms) {
      d.permissions[p] = true;
    }
    data.push(d);
  }
  return data;
}
