<script setup lang="ts">
import type { FullContest } from '@/composables/types';

import { indexToOffset } from './utils';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

const getPid = () => {
  const pid = route.params.pid as string;
  const value = indexToOffset(pid);
  if (value !== undefined) {
    return value;
  } else {
    navigateTo(`/contest/${route.params.id}`);
    return 0;
  }
};

const problem = computed(() => {
  const pid = getPid();
  const offset = 1000;
  return contest.value.problems.find(p => p.display_id === pid + offset);
});

if (problem.value === undefined) {
  await navigateTo(`/contest/${route.params.id}`);
}
</script>

<template>
  <div v-if="problem">
    <problem-content
      :content="problem.problem_info.problem_content"
    ></problem-content>
  </div>
</template>
