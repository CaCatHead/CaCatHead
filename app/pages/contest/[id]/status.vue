<script setup lang="ts">
import type { ContestSubmission } from '@/composables/types';

const route = useRoute();

const { data } = await useFetchAPI<{ submissions: ContestSubmission[] }>(
  `/api/contest/${route.params.id}/status`
);
</script>

<template>
  <div text-sm>
    <c-table :data="data?.submissions ?? []">
      <template #headers>
        <c-table-header name="id" label="#" width="64px"></c-table-header>
        <c-table-header name="created" label="提交时间"></c-table-header>
        <c-table-header name="problem" label="题目"></c-table-header>
        <c-table-header name="language" label="语言"></c-table-header>
        <c-table-header name="verdict" label="结果"></c-table-header>
        <c-table-header name="score" label="得分"></c-table-header>
        <c-table-header name="time_used" label="时间"></c-table-header>
        <c-table-header name="memory_used" label="内存"></c-table-header>
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
      <template #created="{ row }">
        <span>{{ formatDateTime(row.created) }}</span>
      </template>
      <template #problem="{ row }">
        <nuxt-link
          :to="`/contest/${route.params.id}/problem/${displyaIdToIndex(
            row.problem.display_id
          )}/`"
          text-sky-700
          text-op-70
          hover:text-op-100
          >{{ displyaIdToIndex(row.problem.display_id) }}.
          {{ row.problem.title }}</nuxt-link
        >
      </template>
      <template #language="{ row }">{{ row.language }}</template>
      <template #verdict="{ row }">
        <nuxt-link :to="`/contest/${route.params.id}/submission/${row.id}`">
          <verdict :verdict="row.verdict"></verdict>
        </nuxt-link>
      </template>
      <template #time_used="{ row }">
        <span>{{ row.time_used }} ms</span>
      </template>
      <template #memory_used="{ row }">
        <span>{{ row.memory_used }} KB</span>
      </template>
    </c-table>
  </div>
</template>
