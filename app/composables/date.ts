import type { InjectionKey, Ref } from 'vue';

import { format, intervalToDuration } from 'date-fns';

export const formatDateTime = (date: string | Date) =>
  format(new Date(date), 'yyyy-MM-dd HH:mm:ss');

export const formatDateTimeDay = (date: string | Date) =>
  format(new Date(date), 'yyyy-MM-dd');

export const formatDateTimeTime = (date: string | Date) =>
  format(new Date(date), 'HH:mm:ss');

export const formatInterval = (left: Date, right: Date) => {
  const duration = intervalToDuration({
    start: left,
    end: right,
  });
  return duration;
};

export const ServerTimestamp = Symbol('server-timestamp') as InjectionKey<
  Ref<number>
>;

export const useServerTimestamp = () => {
  return inject(ServerTimestamp)!;
};
