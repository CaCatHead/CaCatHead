<script setup lang="ts">
import type { ProblemRepository, FullSubmission } from '@/composables/types';

const props = defineProps<{ repo: ProblemRepository }>();

const { repo } = toRefs(props);

const route = useRoute();

const notify = useNotification();

useHead({
  title: `提交 #${route.params.sid} - ${repo.value?.name}`,
});

const { data } = await useFetchAPI<{
  submission: FullSubmission;
}>(`/api/repo/${route.params.repo}/submission/${route.params.sid}`);

const submission = computed(() => {
  return data.value?.submission!;
});

if (!submission.value) {
  notify.danger('未找到提交或者无访问权限');
  await navigateTo(`/repository/${route.params.repo}/submissions`, {
    replace: true,
  });
}

const rejudge = async () => {};
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
          <c-table-header name="time" label="时间"></c-table-header>
          <c-table-header name="memory" label="内存"></c-table-header>
          <!-- <c-table-header
            v-if="admin"
            name="operation"
            label=""
            width="60px"
          ></c-table-header> -->
        </template>

        <template #id="{ row }">
          <nuxt-link
            :to="`/repository/${route.params.repo}/submission/${row.id}`"
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
            :to="`/repository/${route.params.repo}/problem/${row.problem.display_id}/`"
            text-sky-700
            text-op-70
            hover:text-op-100
            >{{ row.problem.display_id }}. {{ row.problem.title }}</nuxt-link
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
