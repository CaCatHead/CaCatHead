<script setup lang="ts">
const props = withDefaults(defineProps<{ memory: number }>(), {
  memory: 0,
});

const { memory } = toRefs(props);

const formatMB = (memory: number) => {
  const text = (memory / 1024).toFixed(1);
  if (text.endsWith('.0')) {
    return (memory / 1024).toFixed(0);
  } else {
    return text;
  }
};
</script>

<template>
  <span v-if="memory < 1024 * 5">{{ memory }} KB</span>
  <span v-else>{{ formatMB(memory) }} MB</span>
</template>
