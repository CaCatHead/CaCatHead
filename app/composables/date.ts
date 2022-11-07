import { format, intervalToDuration } from 'date-fns';

export const formatDateTime = (date: string | Date) =>
  format(new Date(date), 'yyyy-MM-dd hh:mm:ss');

export const formatInterval = (left: Date, right: Date) => {
  const duration = intervalToDuration({
    start: left,
    end: right,
  });
  return duration;
};
