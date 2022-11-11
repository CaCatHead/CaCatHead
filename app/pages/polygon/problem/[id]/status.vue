<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const { data } = await useFetchAPI<{ sumbissions: any[] }>(
  `/api/polygon/${problem.value.id}/submissions`
);

const submissions = ref(data.value?.sumbissions ?? []);
</script>

<template>
  <div>
    <c-table :data="submissions">
      <template #headers>
        <c-table-header name="id" label="#"></c-table-header>
        <c-table-header name="verdict" label="结果"></c-table-header>
      </template>

      <template #id="{ row }">
        <nuxt-link :to="`/polygon/submission/${row.id}`">{{
          row.id
        }}</nuxt-link>
      </template>
      <template #verdict="{ row }">{{ row.verdict }}</template>
    </c-table>
  </div>
</template>
