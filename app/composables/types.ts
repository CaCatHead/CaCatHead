export interface JudgeNode {
  name: string;

  active: boolean;

  updated: string;

  information: {
    compiler: {
      'g++': string;
      gcc: string;
      java: string;
    };
    platform: {
      system: string;
      machine: string;
      release: string;
      version: string;
      processor: string;
      architecture: [string, string];
    };
  };
}

export interface User {
  id: number;

  username: string;

  nickname: string;
}

export type FullUser = User & {
  permissions: {
    polygon: boolean;
    add_post: boolean;
    add_contest: boolean;
    is_superuser: boolean;
    is_staff: boolean;
  };
};

export interface Team {
  name: string;

  owner: User;

  members: User[];
}

export interface Contest {
  id: number;

  title: string;

  start_time: string;

  end_time: string;

  owner: User;

  is_public: boolean;
}

export type FullContest = Contest & {
  settings: Record<string, boolean>;
  description: string;
  problems: Array<FullPolygonProblem>;
};

export interface Registration {
  name: string;
  team: {
    name: string;
    owner: User;
    members: User[];
  };
  extra_info: Record<string, any>;
}

export interface Post {
  id: number;

  title: string;

  content: string;

  owner: User;

  created: string;

  updated: string;
}

export interface ProblemRepository {
  id: number;

  name: string;
}

export interface Problem {
  display_id: number;
  title: string;
  time_limit: number;
  memory_limit: number;
  is_public: boolean;
}

export type FullProblem = Problem & {
  problem_info: {
    problem_content: ProblemContent;
  };
};

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
  time_limit: number;
  memory_limit: number;

  problem_info: {
    problem_judge: ProblemJudge;
    problem_content: ProblemContent;
  };
}

interface SubmissionDetail {
  compile: {
    stdout: string;
  };
  node: string;
  results: Array<{
    verdict: string;
    time: number;
    memory: number;
    score: number;
    sample?: boolean;
  }>;
  score: number;
  verdict: string;
}

interface BaseSubmission {
  id: number;

  language: string;

  code_length: number;

  created: string;

  judged: string;

  time_used: number;

  memory_used: number;

  verdict: string;

  problem: {
    id?: number;

    display_id: number;

    title: string;
  };
}

export type Submission = BaseSubmission & {
  owner: User;

  judge_node?: string;
};

export type BaseFullSubmission = BaseSubmission & {
  code: string;

  detail: SubmissionDetail;
};

export type FullSubmission = BaseFullSubmission & {
  owner: User;
};

export type ContestSubmission = BaseSubmission & {
  owner: Team;

  relative_time: number;
};

export type FullContestSubmission = BaseFullSubmission & {
  owner: Team;

  relative_time: number;
};

export interface ContestStanding {
  name: string;

  team: Team;

  created: string;

  score: number;

  dirty: number;

  is_participate: boolean;

  standings: {
    submissions: ContestSubmission[];
  };
}
