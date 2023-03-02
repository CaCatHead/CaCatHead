<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const submit = async (payload: { code: string; language: string }) => {
  await fetchAPI(`/api/polygon/${problem.value.display_id}/submit`, {
    method: 'POST',
    body: {
      language: payload.language,
      code: payload.code,
    },
  });
  await navigateTo(`/polygon/problem/${problem.value.display_id}/status`);
};
</script>

<template>
  <div>
    <problem-submit @submit="submit"></problem-submit>
  </div>
</template>
