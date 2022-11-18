import type { Ref } from 'vue-demi';

export const NotificationProviderSymbol = Symbol('notification-provider');

export interface INotification {
  timestamp: Date;
  color: string;
  message: string;
  duration?: number;
}

export interface NotificationContext {
  notifications: Ref<INotification[]>;
}

export interface NotificationOption {
  message?: string;
  color?: string;
  duration?: number;
  variant?: 'light' | 'fill' | 'outline';
}

export const useNotification = () => {
  const ctx = inject<NotificationContext>(NotificationProviderSymbol)!;

  const notify = ({
    message = '',
    color = 'info',
    duration = 3000,
    variant = 'light',
  }: NotificationOption) => {
    const now = new Date();
    ctx.notifications.value.push({
      timestamp: now,
      color,
      message,
    });
    setTimeout(() => {
      const notifications = ctx.notifications.value;
      const idx = notifications.findIndex(n => n.timestamp === now);
      if (idx !== -1) {
        notifications.splice(idx, 1);
      }
    }, duration);
  };

  return {
    notify,
    success(message: string) {
      notify({ message, color: 'success' });
    },
    info(message: string) {
      notify({ message, color: 'info' });
    },
    warning(message: string) {
      notify({ message, color: 'warning' });
    },
    danger(message: string) {
      notify({ message, color: 'danger' });
    },
  };
};
