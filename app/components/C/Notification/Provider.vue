<script setup lang="ts">
import type { INotification } from '@/composables/notify';

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
</script>

<template>
  <div>
    <slot></slot>
    <div fixed top-0 left-0 w-screen h-screen z="-1000" space-y-4 p4>
      <div
        v-for="notification in notifications"
        :key="notification.timestamp.toISOString()"
        flex
        :class="[props.align]"
      >
        <c-notification :color="notification.color">{{
          notification.message
        }}</c-notification>
      </div>
    </div>
  </div>
</template>
