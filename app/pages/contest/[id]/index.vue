<script setup lang="ts">
import type { FullContest } from '@/composables/types';
import { displyaIdToIndex } from '@/composables/contest';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `面板 - ${contest.value.title}`,
});
</script>

<template>
  <div>
    <contest-layout :contest="contest">
      <c-table :data="contest.problems" border="1 base" rounded-2>
        <template #headers>
          <c-table-header
            name="display_id"
            width="80"
            row-class="border-r-1 border-base"
            class="border-r-1 border-base"
            >#</c-table-header
          >
          <c-table-header
            name="title"
            align="left"
            text-left
            row-class="px4"
            class="px4"
            >标题</c-table-header
          >
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
          <nuxt-link
            :to="`/contest/${route.params.id}/problem/${displyaIdToIndex(
              row.display_id
            )}`"
            class="text-link"
            >{{ row.title }}</nuxt-link
          >
        </template>
      </c-table>

      <div mt12>
        <div font-bold text-xl flex items-center>
          <span i-carbon-information text-2xl></span>
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
