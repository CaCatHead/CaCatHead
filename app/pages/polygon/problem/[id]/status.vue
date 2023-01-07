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
        <c-table-header name="id" label="#" width="64px"></c-table-header>
        <c-table-header name="created" label="提交时间"></c-table-header>
        <c-table-header name="owner" label="用户"></c-table-header>
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
        <div>{{ formatDateTimeDay(row.created) }}</div>
        <div>{{ formatDateTimeTime(row.created) }}</div>
      </template>
      <template #owner="{ row }">
        <user-link :user="row.owner"></user-link>
      </template>
      <template #problem="{ row }">
        <nuxt-link
          :to="`/polygon/problem/${problem.id}/`"
          text-sky-700
          text-op-70
          hover:text-op-100
          >#{{ problem.id }}. {{ problem.title }}</nuxt-link
        >
      </template>
      <template #language="{ row }">{{ row.language }}</template>
      <template #verdict="{ row }">
        <nuxt-link :to="`/polygon/submission/${row.id}`">
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
