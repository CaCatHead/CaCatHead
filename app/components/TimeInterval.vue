<script setup lang="ts">
const props = defineProps<{
  left: string | Date;
  right?: string | Date;
}>();
const { left, right } = toRefs(props);

const duration = computed(() => {
  return formatInterval(
    new Date(left.value),
    new Date(right?.value ?? new Date())
  );
});
</script>

<template>
  <span>
    <span v-if="!!duration.years">&nbsp;{{ duration.years }} 年</span>
    <span v-if="!!duration.months">&nbsp;{{ duration.months }} 月</span>
    <span v-if="!!duration.days">&nbsp;{{ duration.days }} 天</span>
    <span v-if="!!duration.hours">&nbsp;{{ duration.hours }} 小时</span>
    <span
      v-if="
        duration.years || duration.months || duration.days || duration.hours
      "
      >前</span
    >
    <span v-else>
      <span v-if="!!duration.minutes">&nbsp;{{ duration.minutes }} 分钟前</span>
      <span v-else>刚刚</span>
    </span>
  </span>
</template>
