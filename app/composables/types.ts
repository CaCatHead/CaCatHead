export interface Post {
  id: number;

  title: string;

  content: string;

  owner: {
    id: number;
    username: string;
    nickname: string;
  };

  created: string;

  updated: string;
}
