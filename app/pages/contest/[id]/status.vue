<script setup lang="ts">
import type { FullContest, ContestSubmission } from '@/composables/types';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `我的提交 - ${contest.value.title}`,
});

const { data } = await useFetchAPI<{ submissions: ContestSubmission[] }>(
  `/api/contest/${route.params.id}/status`
);
</script>

<template>
  <contest-layout :contest="contest">
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
            <verdict :verdict="row.verdict"></verdict>
          </nuxt-link>
        </template>
        <template #time_used="{ row }">
          <span>{{ row.time_used }} ms</span>
        </template>
        <template #memory_used="{ row }">
          <display-memory :memory="row.memory_used"></display-memory>
        </template>
      </c-table>
    </div>
  </contest-layout>
</template>
