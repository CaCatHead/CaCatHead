<script setup lang="ts">
import type { ProblemRepository } from '@/composables/types';

const props = defineProps<{ repo: ProblemRepository }>();

const { repo } = toRefs(props);

useHead({
  title: `题目集 - ${repo.value.name}`,
});

const route = useRoute();

const { data } = await useFetchAPI<{
  problems: any[];
}>(`/api/repo/${route.params.repo}/problems`);

const problems = computed(() => data.value?.problems ?? []);
</script>

<template>
  <div w-full>
    <c-table :data="problems" border>
      <template #headers>
        <c-table-header
          name="id"
          label="#"
          width="80"
          row-class="text-center"
        ></c-table-header>
        <c-table-header name="title" label="标题"></c-table-header>
      </template>

      <template #id="{ row }">
        <span font-bold>{{ row.display_id }}</span>
      </template>
      <template #title="{ row }">
        <nuxt-link
          :to="`/repository/${route.params.repo}/problem/${row.display_id}/`"
          text-sky-700
          text-op-80
          hover:text-op-100
          >{{ row.title }}</nuxt-link
        >
      </template>

      <template #empty>
        <div h="36" text-xl font-bold flex items-center justify-center>
          没有题目
        </div>
      </template>
    </c-table>
  </div>
</template>
