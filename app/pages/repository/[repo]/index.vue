<script setup lang="ts">
import type { ProblemRepository } from '@/composables/types';

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
</script>

<template>
  <div w-full>
    <problem-list
      :problems="problems"
      :problem-link="
        row => `/repository/${route.params.repo}/problem/${row.display_id}`
      "
    ></problem-list>
  </div>
</template>
