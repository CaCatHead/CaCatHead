<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);
</script>

<template>
  <div>
    <h2 text-2xl font-bold>{{ problem.id }}. {{ problem.title }}</h2>
  </div>
</template>
