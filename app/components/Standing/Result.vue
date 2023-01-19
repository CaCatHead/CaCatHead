<script setup lang="ts">
defineProps<{
  result:
    | {
        ok: boolean;
        time: number;
        dirty: number;
        first: boolean;
        practice?: boolean;
      }
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
  <div
    v-if="result"
    sm:p4
    select-none
    cursor-pointer
    :class="[result.first && 'bg-[#E0FFE4]']"
  >
    <div v-if="result.ok" inline-block>
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
      <div class="sm:text-center font-bold text-red-500">
        <span>-</span>
        <span>{{ result.dirty }}</span>
      </div>
    </div>
  </div>
</template>
