<script setup lang="ts">
import type { ProblemRepository, Submission } from '@/composables/types';

const props = defineProps<{ repo: ProblemRepository }>();

const { repo } = toRefs(props);

useHead({
  title: `所有提交 - ${repo.value.name}`,
});

const route = useRoute();

const page = computed(() => +(route.query.page ?? 1));

const { data } = await useFetchAPI<{
  submissions: Submission[];
  count: number;
  page: number;
  page_size: number;
  num_pages: number;
}>(`/api/repo/${route.params.repo}/submissions`, {
  query: {
    page,
  },
});

const handlePageChange = async (toPage: number) => {
  await navigateTo({ path: route.path, query: { page: toPage + 1 } });
};
</script>

<template>
  <div w-full>
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
          <c-table-header
            name="score"
            label="得分"
            width="60px"
          ></c-table-header>
          <c-table-header name="time_used" label="时间"></c-table-header>
          <c-table-header name="memory_used" label="内存"></c-table-header>
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
          <div text-xs>{{ formatDateTimeDay(row.created) }}</div>
          <div text-xs>{{ formatDateTimeTime(row.created) }}</div>
        </template>
        <template #team="{ row }">
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
          <nuxt-link
            :to="`/repository/${route.params.repo}/submission/${row.id}`"
          >
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
  </div>
</template>
