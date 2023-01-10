<script setup lang="ts">
import type { FullProblem } from '@/composables/types';

const route = useRoute();

const { data } = await useFetchAPI<{ problem: FullProblem }>(
  `/api/repo/${route.params.repo}/problem/${route.params.problem}`
);

if (!data) {
  await navigateTo('/repository');
}

const problem = ref(data.value!.problem);
</script>

<template>
  <div class="w-full">
    <Head>
      <Title>{{ problem.title }}</Title>
    </Head>

    <div prose prose-truegray>
      <h2>{{ problem.display_id }}. {{ problem.title }}</h2>
    </div>

    <problem-content
      :content="problem.problem_info.problem_content"
      :time="problem.time_limit"
      :memory="problem.memory_limit"
    ></problem-content>
  </div>
</template>
