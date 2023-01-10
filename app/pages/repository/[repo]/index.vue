<script setup lang="ts">
import type { ProblemRepository, Problem } from '@/composables/types';

const props = defineProps<{ repo: ProblemRepository }>();

const { repo } = toRefs(props);

useHead({
  title: `题目集 - ${repo.value?.name}`,
});

const route = useRoute();

const { data } = await useFetchAPI<{
  problems: any[];
}>(`/api/repo/${route.params.repo}/problems`);

const problems = computed(() => data.value?.problems ?? []);

const lastProblem = useRepoLastProblem(route.params.repo);

const goSubmit = async (problem: Problem) => {
  lastProblem.value = problem.display_id;
  await navigateTo(`/repository/${route.params.repo}/submit`);
};
</script>

<template>
  <div w-full>
    <problem-list
      :problems="problems"
      :problem-link="
        row => `/repository/${route.params.repo}/problem/${row.display_id}`
      "
      @submit="goSubmit"
    ></problem-list>
  </div>
</template>
