export interface User {
  id: number;

  username: string;

  nickname: string;
}

export type FullUser = User & {
  permissions: { polygon: boolean; add_post: boolean; add_contest: boolean };
};

export interface Contest {
  id: number;

  title: string;

  start_time: string;

  end_time: string;
}

export type FullContest = Contest & { problems: Array<FullPolygonProblem> };

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

export interface ProblemJudge {
  testcase_detail: Array<{
    input: string;
    answer: string;
    score: number;
    sample?: boolean;
  }>;
}

export interface FullPolygonProblem {
  id: number;
  display_id: number;
  title: string;
  is_public: boolean;
  owner: User;
  problem_type: 'classic_ac';

  problem_info: {
    problem_judge: ProblemJudge;
    problem_content: ProblemContent;
  };
}
