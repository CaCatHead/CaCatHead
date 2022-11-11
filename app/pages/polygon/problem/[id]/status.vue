<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const { data } = await useFetchAPI<{ submissions: any[] }>(
  `/api/polygon/${problem.value.id}/submissions`
);

const submissions = ref(data.value?.submissions ?? []);
</script>

<template>
  <div>
    <c-table :data="submissions">
      <template #headers>
        <c-table-header
          name="id"
          label="#"
          width="64px"
          row-class="text-center"
        ></c-table-header>
        <c-table-header
          name="verdict"
          label="结果"
          row-class="text-center"
        ></c-table-header>
      </template>

      <template #id="{ row }">
        <nuxt-link
          :to="`/polygon/submission/${row.id}`"
          text-sky-700
          text-op-70
          hover:text-op-100
          >{{ row.id }}</nuxt-link
        >
      </template>
      <template #verdict="{ row }">{{ row.verdict }}</template>
    </c-table>
  </div>
</template>
