export enum Verdict {
  Waiting = 'Waiting',
  Running = 'Running',
  Compiling = 'Compiling',
  Accepted = 'Accepted',
  WrongAnswer = 'WrongAnswer',
  TimeLimitExceeded = 'TimeLimitExceeded',
  IdlenessLimitExceeded = 'IdlenessLimitExceeded',
  MemoryLimitExceeded = 'MemoryLimitExceeded',
  OutputLimitExceeded = 'OutputLimitExceeded',
  RuntimeError = 'RuntimeError',
  Point = 'Point',
  PartiallyCorrect = 'PartiallyCorrect',
  CompileError = 'CompileError',
  SystemError = 'SystemError',
  JudgeError = 'JudgeError',
  TestCaseError = 'TestCaseError',
}