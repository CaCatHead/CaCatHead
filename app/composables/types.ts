export interface User {
  id: number;

  username: string;

  nickname: string;
}

export interface Post {
  id: number;

  title: string;

  content: string;

  owner: User;

  created: string;

  updated: string;
}
