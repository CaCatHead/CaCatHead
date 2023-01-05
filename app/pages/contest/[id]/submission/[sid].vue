<script setup lang="ts">
import type { FullContestSubmission } from '@/composables/types';

const route = useRoute();

const { data } = await useFetchAPI<{ submission: FullContestSubmission }>(
  `/api/contest/${route.params.id}/submission/${route.params.sid}`
);

const submission = computed(() => {
  return data.value?.submission!;
});

if (!submission.value) {
  await navigateTo(`/contest/${route.params.id}/status`);
}
</script>

<template>
  <div space-y-4>
    <div shadow-box rounded>
      <c-table :data="[submission]">
        <template #headers>
          <c-table-header name="id" label="#" width="64px"></c-table-header>
          <c-table-header name="created" label="提交时间"></c-table-header>
          <c-table-header name="owner" label="用户"></c-table-header>
          <c-table-header name="problem" label="题目"></c-table-header>
          <c-table-header name="language" label="语言"></c-table-header>
          <c-table-header name="verdict" label="结果"></c-table-header>
          <c-table-header name="score" label="得分"></c-table-header>
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
        <template #owner="{ row }">
          <team-link :team="row.owner"></team-link>
        </template>
        <template #problem="{ row }">
          <span>{{ row.problem.title }}</span>
        </template>
        <template #language="{ row }">{{ row.language }}</template>
        <template #verdict="{ row }">
          <verdict :verdict="row.verdict"></verdict>
        </template>
      </c-table>
    </div>
    <pre font-mono p4 shadow-box rounded overflow-auto>{{
      submission.code
    }}</pre>
    <pre font-mono p4 shadow-box rounded overflow-auto>{{
      JSON.stringify(submission.detail, null, 2)
    }}</pre>
  </div>
</template>
