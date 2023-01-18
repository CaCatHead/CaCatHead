<script setup lang="ts">
import type { FullContest, ContestSubmission } from '@/composables/types';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `所有提交 - ${contest.value.title}`,
});

const page = computed(() => +(route.query.page ?? 1));
const verdict = computed(() => route.query.verdict ?? undefined);
const problem = computed(() => {
  if (route.query.problem === undefined || route.query.problem === null) {
    return undefined;
  }
  const id = indexToDisplayId(route.query.problem as string);
  if (id !== undefined) {
    return id;
  } else {
    navigateTo(route.path);
    return undefined;
  }
});

const { data } = await useFetchAPI<{
  submissions: ContestSubmission[];
  count: number;
  page: number;
  page_size: number;
  num_pages: number;
}>(`/api/contest/${route.params.id}/submissions`, {
  query: {
    page,
    verdict,
    problem,
  },
});

const handleFilter = async (payload: {
  verdict?: string | undefined;
  problem?: string | undefined;
}) => {
  const query: Record<string, string> = {};
  if (payload.verdict) {
    query['verdict'] = payload.verdict;
  }
  if (payload.problem) {
    query['problem'] = payload.problem;
  }

  await navigateTo({
    path: route.path,
    query,
  });
};

const handlePageChange = async (toPage: number) => {
  await navigateTo({
    path: route.path,
    query: { page: toPage + 1, verdict: verdict.value, problem: problem.value },
  });
};
</script>

<template>
  <contest-layout :contest="contest" @filter="handleFilter">
    <div text-sm>
      <c-table :data="data?.submissions ?? []">
        <template #headers>
          <c-table-header name="id" label="#" width="64px"></c-table-header>
          <c-table-header
            name="created"
            label="提交时间"
            width="96px"
          ></c-table-header>
          <c-table-header name="problem" label="题目"></c-table-header>
          <c-table-header name="team" label="队伍"></c-table-header>
          <c-table-header
            name="language"
            label="语言"
            width="48px"
          ></c-table-header>
          <c-table-header name="verdict" label="结果"></c-table-header>
          <!-- <c-table-header
            name="score"
            label="得分"
            width="60px"
          ></c-table-header> -->
          <c-table-header name="time_used" label="时间"></c-table-header>
          <c-table-header name="memory_used" label="内存"></c-table-header>
        </template>

        <template #id="{ row }">
          <nuxt-link
            :to="`/contest/${route.params.id}/submission/${row.id}`"
            text-sky-700
            text-op-70
            hover:text-op-100
            >{{ row.id }}</nuxt-link
          >
        </template>
        <template #created="{ row }">
          <div text-xs>{{ formatDateTimeDay(row.created) }}</div>
          <div text-xs>{{ formatDateTimeTime(row.created) }}</div>
        </template>
        <template #team="{ row }">
          <team-link :team="row.owner"></team-link>
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
        <template #language="{ row }"
          ><display-language :language="row.language"
        /></template>
        <template #verdict="{ row }">
          <nuxt-link :to="`/contest/${route.params.id}/submission/${row.id}`">
            <display-verdict :verdict="row.verdict"></display-verdict>
          </nuxt-link>
        </template>
        <template #time_used="{ row }">
          <span>{{ row.time_used }} ms</span>
        </template>
        <template #memory_used="{ row }">
          <display-memory :memory="row.memory_used"></display-memory>
        </template>
      </c-table>

      <c-table-page
        mt4
        v-if="(data?.num_pages ?? 1) > 1"
        :count="data!.count"
        :page="page - 1"
        :page-size="data!.page_size"
        @change="handlePageChange"
      ></c-table-page>
    </div>
  </contest-layout>
</template>
