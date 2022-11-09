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

export interface PolygonProblem {
  id: number;
  display_id: number;
  title: string;
  is_public: boolean;
  owner: User;
  problem_type: 'classic_ac';
}

export interface ProblemContent {
  title: string;
  description: string;
  input: string;
  output: string;
  sample: Array<{ input: string; answer: string }>;
  hint: string;
  source: string;
}

export interface FullPolygonProblem {
  id: number;
  display_id: number;
  title: string;
  is_public: boolean;
  owner: User;
  problem_type: 'classic_ac';

  problem_info: {
    problem_content: ProblemContent;
  };
}
