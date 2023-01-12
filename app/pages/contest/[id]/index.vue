<script setup lang="ts">
import type { FullContest, Problem } from '@/composables/types';

import { displyaIdToIndex } from '@/composables/contest';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `面板 - ${contest.value.title}`,
});

const lastProblem = useContestLastProblem(route.params.id);
const goSubmit = async (problem: Problem) => {
  lastProblem.value = problem.display_id;
  await navigateTo(`/contest/${route.params.id}/submit`);
};
</script>

<template>
  <div>
    <contest-layout :contest="contest">
      <problem-list
        :problems="contest.problems"
        :problem-index="row => displyaIdToIndex(row.display_id)"
        :problem-link="
          row =>
            `/contest/${route.params.id}/problem/${displyaIdToIndex(
              row.display_id
            )}`
        "
        @submit="goSubmit"
      ></problem-list>

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
