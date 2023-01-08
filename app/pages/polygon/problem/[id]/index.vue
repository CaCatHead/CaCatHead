<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);
</script>

<template>
  <div>
    <ProblemContent
      :time="problem.time_limit"
      :memory="problem.memory_limit"
      :content="problem.problem_info.problem_content"
    ></ProblemContent>
  </div>
</template>
