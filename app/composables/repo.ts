export const useRepoLastProblem = (id: string | string[]) =>
  useLocalStorage(`repo/${id}/last-problem`, 1000);
