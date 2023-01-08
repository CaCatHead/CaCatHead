<script setup lang="ts">
const props = withDefaults(defineProps<{ memory: number }>(), {
  memory: 0,
});

const { memory } = toRefs(props);
</script>

<template>
  <span v-if="memory < 1024 * 5">{{ memory }} KB</span>
  <span v-else>{{ (memory / 1024).toFixed(1) }} MB</span>
</template>
