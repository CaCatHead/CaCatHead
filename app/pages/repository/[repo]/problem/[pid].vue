<script setup lang="ts">
import type { FullProblem } from '@/composables/types';

const route = useRoute();

const { data } = await useFetchAPI<{ problem: FullProblem }>(
  `/api/repo/${route.params.repo}/problem/${route.params.pid}`
);

if (!data) {
  await navigateTo('/repository');
}

const problem = computed(() => data.value!.problem);

useHead({
  title: `#${problem.value.display_id}. ${problem.value.title}`,
});

useRepoLastProblem(route.params.repo).value = problem.value.display_id;
</script>

<template>
  <div v-if="problem" class="w-full">
    <div text-left mb4>
      <h3 font-bold text-2xl>{{ problem.display_id }}. {{ problem.title }}</h3>
    </div>

    <problem-content
      :content="problem.problem_info.problem_content"
      :time="problem.time_limit"
      :memory="problem.memory_limit"
    ></problem-content>
  </div>
</template>
