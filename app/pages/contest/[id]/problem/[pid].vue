<script setup lang="ts">
import type { FullContest } from '@/composables/types';

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

useLocalStorage(
  `contest/${route.params.id}/last-problem`,
  problem.value?.display_id
).value = problem.value?.display_id;
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
