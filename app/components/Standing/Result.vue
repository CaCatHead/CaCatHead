<script setup lang="ts">
defineProps<{
  result:
    | { ok: boolean; time: number; dirty: number; practice?: boolean }
    | undefined;
}>();

function toNumDuration(seconds: number) {
  function alignNumber(value: number) {
    return (value < 10 ? '0' : '') + value;
  }
  const hour = Math.floor(seconds / 3600);
  const minute = Math.floor((seconds % 3600) / 60);
  return `${hour}:${alignNumber(minute)}`;
}
</script>

<template>
  <div v-if="result" p4 select-none cursor-pointer>
    <div v-if="result.ok">
      <div
        :class="[
          'text-center',
          'font-bold',
          !result.practice ? 'text-green-500' : 'text-blue-500',
        ]"
      >
        <span>+</span>
        <span v-if="result.dirty">{{ result.dirty }}</span>
      </div>
      <div v-if="!result.practice" class="text-sm text-gray-400">
        <span>{{ toNumDuration(result.time) }}</span>
      </div>
    </div>
    <div v-else-if="!!result.dirty">
      <div class="text-center font-bold text-red-500">
        <span>-</span>
        <span>{{ result.dirty }}</span>
      </div>
    </div>
  </div>
</template>
