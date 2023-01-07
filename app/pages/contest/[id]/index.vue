<script setup lang="ts">
import type { FullContest } from '@/composables/types';
import { displyaIdToIndex } from '@/composables/contest';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `面板 - ${contest.value.title}`,
});

const lastProblem = useContestLastProblem(route.params.id);
const goSubmit = async (id: number) => {
  lastProblem.value = id;
  await navigateTo(`/contest/${route.params.id}/submit`);
};
</script>

<template>
  <div>
    <contest-layout :contest="contest">
      <c-table :data="contest.problems" border="1 base" rounded-2>
        <template #headers>
          <c-table-header
            name="display_id"
            width="60"
            row-class="border-r-1 border-base"
            class="border-r-1 border-base bg-gray-100 dark:bg-dark-100"
            >#</c-table-header
          >
          <c-table-header
            name="title"
            align="left"
            text-left
            row-class="px4 border-r-1 border-base"
            class="border-r-1 border-base px4 bg-gray-100 dark:bg-dark-100"
            >题目</c-table-header
          >
          <c-table-header
            name="operation"
            class="border-r-1 border-base bg-gray-100 dark:bg-dark-100"
            width="60px"
            ><span></span
          ></c-table-header>
        </template>
        <template #display_id="{ row }">
          <nuxt-link
            :to="`/contest/${route.params.id}/problem/${displyaIdToIndex(
              row.display_id
            )}`"
            class="text-link"
            >{{ displyaIdToIndex(row.display_id) }}</nuxt-link
          ></template
        >
        <template #title="{ row }">
          <div
            flex
            justify-between
            items-center
            lt-md="items-start flex-col gap1"
          >
            <nuxt-link
              :to="`/contest/${route.params.id}/problem/${displyaIdToIndex(
                row.display_id
              )}`"
              class="text-link"
              >{{ row.title }}</nuxt-link
            >
            <div
              text-xs
              text-base-800
              text-op-60
              inline-flex
              items-end
              md="flex-col w-32 gap1"
              lt-md="gap2"
            >
              <span inline-flex items-center justify-start>
                <span i-carbon-time text-lg mr1></span>
                <span>{{ row.time_limit }} ms</span>
              </span>
              <span inline-flex items-center justify-start>
                <span i-carbon-chip text-lg mr1></span>
                <span>{{ row.memory_limit }} KB</span>
              </span>
            </div>
          </div>
        </template>
        <template #operation="{ row }">
          <c-button
            variant="text"
            color="success"
            icon="i-carbon-cloud-upload"
            @click="goSubmit(row.display_id)"
          ></c-button>
        </template>
      </c-table>

      <div mt12>
        <div font-bold text-xl flex items-center>
          <span i-carbon-bullhorn text-3xl></span>
          <span ml2>比赛公告</span>
        </div>
        <div mt4>
          <c-markdown :content="contest.description"></c-markdown>
        </div>
      </div>

      <div mt8>
        <div font-bold text-xl flex items-center>
          <span i-carbon-information text-3xl></span>
          <span ml2>比赛信息</span>
        </div>
        <ul mt4 space-y-2>
          <li>
            <span font-bold mr2>开始时间:</span
            ><span>{{ formatDateTime(contest.start_time) }}</span>
          </li>
          <li>
            <span font-bold mr2>持续时间:</span>
            <span>{{ formatContestDuration(contest) }}</span>
          </li>
        </ul>
      </div>
    </contest-layout>
  </div>
</template>
