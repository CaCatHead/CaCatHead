<script setup lang="ts">
defineProps<{
  type: 'icpc' | 'ioi';
  result:
    | {
        ok: boolean;
        time: number;
        score: number;
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
    sm:p2
    select-none
    cursor-pointer
    :class="[
      'w-full',
      'inline-block',
      result.first && 'bg-[#E0FFE4] dark:bg-[#065c00]',
    ]"
  >
    <div v-if="result.ok" inline-block>
      <div
        :class="[
          'text-center',
          'font-bold',
          !result.practice ? 'text-green-500' : 'text-blue-500',
        ]"
      >
        <span v-if="type === 'icpc'"
          >+{{ result.dirty ? result.dirty : '' }}</span
        >
        <span v-else-if="type === 'ioi'">{{ result.score }}</span>
      </div>
      <div v-if="!result.practice" class="text-[10px] text-gray-400">
        <span>{{ toNumDuration(result.time) }}</span>
      </div>
    </div>
    <div v-else-if="!!result.dirty">
      <div class="sm:text-center font-bold text-red-500">
        <span v-if="type === 'icpc'">-{{ result.dirty }}</span>
        <span v-else-if="type === 'ioi'">{{ result.score }}</span>
      </div>
    </div>
  </div>
</template>
