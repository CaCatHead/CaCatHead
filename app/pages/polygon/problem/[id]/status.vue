<script setup lang="ts">
import type { FullPolygonProblem, Submission } from '@/composables/types';

const notify = useNotification();

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const { data, refresh } = await useFetchAPI<{ submissions: Submission[] }>(
  `/api/polygon/${problem.value.display_id}/submissions`
);

const submissions = computed(() => data.value?.submissions ?? []);

const rejudge = async (submission: Submission) => {
  try {
    await fetchAPI(`/api/polygon/submission/${submission.id}/rejudge`, {
      method: 'POST',
    });
    notify.success(`提交 #${submission.id}. 发起重测成功`);
    await refresh();
  } catch {
    notify.danger(`提交 #${submission.id}. 发起重测失败`);
  }
};
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
        <c-table-header name="node" label="评测机"></c-table-header>
        <c-table-header name="operation" label="" width="60px"></c-table-header>
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
        <div text-sm>{{ formatDateTimeDay(row.created) }}</div>
        <div text-sm>{{ formatDateTimeTime(row.created) }}</div>
      </template>
      <template #owner="{ row }">
        <user-link :user="row.owner"></user-link>
      </template>
      <template #problem="{ row }">
        <nuxt-link
          :to="`/polygon/problem/${problem.display_id}/`"
          text-sky-700
          text-op-70
          hover:text-op-100
          >#{{ problem.display_id }}. {{ problem.title }}</nuxt-link
        >
      </template>
      <template #language="{ row }"
        ><display-language :language="row.language"
      /></template>
      <template #verdict="{ row }">
        <nuxt-link :to="`/polygon/submission/${row.id}`">
          <display-verdict :verdict="row.verdict"></display-verdict>
        </nuxt-link>
      </template>
      <template #time_used="{ row }">
        <span>{{ row.time_used }} ms</span>
      </template>
      <template #memory_used="{ row }">
        <display-memory :memory="row.memory_used"></display-memory>
      </template>
      <template #node="{ row }">
        <span>{{ row.judge_node }}</span>
      </template>
      <template #operation="{ row }">
        <div inline-flex lt-md:mr="-4">
          <c-button variant="text" color="warning" @click="rejudge(row)"
            >重测</c-button
          >
        </div>
      </template>
    </c-table>
  </div>
</template>
