<script setup lang="ts">
import type { INotification } from '@/composables/notify';

import { useAutoAnimate } from '@formkit/auto-animate/vue';

const props = withDefaults(
  defineProps<{
    align?: 'justify-center' | 'justify-start' | 'justify-end';
  }>(),
  { align: 'justify-center' }
);

const notifications = ref<INotification[]>([]);

provide(NotificationProviderSymbol, {
  notifications,
});

const [parent] = useAutoAnimate();
</script>

<template>
  <div>
    <slot></slot>
    <div fixed top-0 left-0 w-screen ref="parent" style="pointer-events: none">
      <div
        v-for="notification in notifications"
        :key="notification.timestamp.toISOString()"
        mt2
        flex
        justify-center
        style="pointer-events: none"
      >
        <c-notification :color="notification.color" z="1000">{{
          notification.message
        }}</c-notification>
      </div>
    </div>
  </div>
</template>
