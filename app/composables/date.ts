import { format } from 'date-fns';

export const formatDateTime = (date: string | Date) =>
  format(new Date(date), 'yyyy-MM-dd hh:mm:ss');
