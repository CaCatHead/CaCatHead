<script setup lang="ts">
import type { FullSubmission } from '@/composables/types';

const route = useRoute();

const notify = useNotification();

useHead({
  title: 'Submission #' + route.params.id,
});

const { data, refresh } = await useFetchAPI<{ submission: FullSubmission }>(
  `/api/polygon/submission/${route.params.id}`
);

if (data.value === null) {
  await navigateTo(`/polygon`, { replace: true });
}

const submission = computed(() => data.value!.submission);

const rejudge = async () => {
  try {
    await fetchAPI(`/api/polygon/submission/${submission.value.id}/rejudge`, {
      method: 'POST',
    });
    notify.success(`提交 #${submission.value.id}. 发起重测成功`);
    await refresh();
  } catch {
    notify.danger(`提交 #${submission.value.id}. 发起重测失败`);
  }
};
</script>

<template>
  <div>
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
          <c-table-header name="time" label="时间"></c-table-header>
          <c-table-header name="memory" label="内存"></c-table-header>
          <c-table-header
            name="operation"
            label=""
            width="60px"
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
        <template #created="{ row }">
          <span>{{ formatDateTime(row.created) }}</span>
        </template>
        <template #owner="{ row }">
          <user-link :user="row.owner"></user-link>
        </template>
        <template #problem="{ row }">
          <nuxt-link
            :to="`/polygon/problem/${row.problem.id}`"
            text-sky-700
            text-op-70
            hover:text-op-100
            >#{{ row.problem.id }}. {{ row.problem.title }}</nuxt-link
          >
        </template>
        <template #language="{ row }"
          ><display-language :language="row.language"
        /></template>
        <template #verdict="{ row }">
          <display-verdict :verdict="row.verdict"></display-verdict>
        </template>
        <template #time="{ row }">{{ row.time_used }} ms</template>
        <template #memory="{ row }"
          ><display-memory :memory="row.memory_used"></display-memory
        ></template>
        <template #operation>
          <div lt-md:mr="-4">
            <c-button variant="text" color="warning" @click="rejudge"
              >重测</c-button
            >
          </div>
        </template>
      </c-table>
    </div>
    <submission-detail :submission="submission"></submission-detail>
  </div>
</template>
