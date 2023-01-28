<script setup lang="ts">
import type { FullContest, Team } from '@/composables/types';

const notify = useNotification();

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `Rating - ${contest.value.title}`,
});

interface RatingLog {
  team: Team;
  old_rating: number;
  delta: number;
}

const { data, refresh } = useFetchAPI<{ logs: RatingLog[] }>(
  `/api/contest/${route.params.id}/rating`
);

const deltaSum = computed(() => {
  const logs = data.value?.logs ?? [];
  let sum = 0;
  for (const log of logs) {
    sum += log.delta;
  }
  return sum;
});

const refreshRating = useThrottleFn(async () => {
  try {
    await fetchAPI(`/api/contest/${route.params.id}/rating`, {
      method: 'POST',
    });
    notify.success(`比赛 ${contest.value.title} 刷新 Rating 成功`);
    await refresh();
  } catch (err) {
    notify.danger(`比赛 ${contest.value.title} 刷新 Rating 失败`);
  }
}, 10000);

const deleteRating = async () => {
  try {
    await fetchAPI(`/api/contest/${route.params.id}/rating`, {
      method: 'DELETE',
    });
    notify.success(`比赛 ${contest.value.title} 删除 Rating 成功`);
    await refresh();
  } catch (err) {
    notify.danger(`比赛 ${contest.value.title} 删除 Rating 失败`);
  }
};
</script>

<template>
  <div space-y-4>
    <div space-x-2>
      <c-button color="info" @click="refreshRating">刷新 Rating</c-button>
      <c-button color="danger" @click="deleteRating">删除 Rating</c-button>
    </div>
    <div>
      <c-table :data="data?.logs ?? []" :mobile="false">
        <template #headers>
          <c-table-header name="index">#</c-table-header>
          <c-table-header name="team">队伍</c-table-header>
          <c-table-header name="rating">Rating</c-table-header>
        </template>

        <template #index="{ index }"
          ><span font-bold>{{ index + 1 }}</span></template
        >
        <template #team="{ row }"
          ><team-link :team="row.team"></team-link
        ></template>
        <template #rating="{ row }">
          <div flex items-center justify-center gap1>
            <display-rating :rating="row.old_rating">{{
              row.old_rating
            }}</display-rating>
            <span i-carbon-arrow-right></span>
            <display-rating :rating="row.old_rating + row.delta">{{
              row.old_rating + row.delta
            }}</display-rating>
          </div>
        </template>

        <template #empty>
          <div h-36 font-bold flex items-center justify-center>
            没有 Rating 更新记录
          </div>
        </template>
      </c-table>
    </div>
    <div v-if="data?.logs && data.logs.length > 0" text-right>
      <span text-gray-500>Rating 变化量</span>
      <span ml2 font-bold>{{ deltaSum }}</span>
    </div>
  </div>
</template>
