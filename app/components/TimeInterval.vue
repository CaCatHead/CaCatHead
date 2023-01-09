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

const text = computed(() => {
  const arr: string[] = [];
  if (duration.value.years) {
    arr.push(`${duration.value.years} 年`);
  }
  if (duration.value.months) {
    arr.push(`${duration.value.months} 个月`);
  }
  if (duration.value.days) {
    arr.push(`${duration.value.days} 天`);
  }
  if (duration.value.hours) {
    arr.push(`${duration.value.hours} 小时`);
  }
  if (duration.value.minutes) {
    arr.push(`${duration.value.minutes} 分钟`);
  }
  if (arr.length > 0) {
    return ' ' + arr.join(' ') + '前';
  } else {
    return '刚刚';
  }
});
</script>

<template>
  <span>{{ text }}</span>
</template>
