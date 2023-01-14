<script setup lang="ts">
import type { FullContest } from '@/composables/types';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

const pid = computed(() => {
  const pid = route.params.pid as string;
  const value = parseProblemIndex(pid);
  if (value !== undefined) {
    return value;
  } else {
    navigateTo(`/contest/${route.params.id}`);
    return 0;
  }
});

const problem = computed(() => {
  return contest.value.problems.find(p => p.display_id === pid.value);
});

if (problem.value === undefined) {
  await navigateTo(`/contest/${route.params.id}`);
}

useContestLastProblem(route.params.id).value = problem.value?.display_id;

useHead({
  title: `${route.params.pid}. ${problem.value?.title} - ${contest.value.title}`,
});
</script>

<template>
  <contest-layout :contest="contest">
    <div v-if="problem">
      <div text-left mb4>
        <h3 font-bold text-2xl>{{ route.params.pid }}. {{ problem.title }}</h3>
      </div>
      <problem-content
        :time="problem.time_limit"
        :memory="problem.memory_limit"
        :content="problem.problem_info.problem_content"
      ></problem-content>
    </div>
  </contest-layout>
</template>
