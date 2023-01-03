<script setup lang="ts">
import type { Contest } from '@/composables/types';

const route = useRoute();

const { data: contest } = await useFetchAPI<{ contest: Contest }>(
  `/api/contest/${route.params.id}/content`
);

if (contest !== null) {
  useHead({
    title: `比赛 ${contest.value?.contest.title}`,
  });
}
</script>

<template>
  <div v-if="contest">
    <h3 font-bold text-xl>{{ contest.contest.title }}</h3>
  </div>
</template>
