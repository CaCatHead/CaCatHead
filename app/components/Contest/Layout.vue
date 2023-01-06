<script setup lang="ts">
import type { FullContest } from '@/composables/types';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

const timestamp = useTimestamp({ offset: 1000 });
const duration = getContestDuration(contest.value) * 60;
const startTime = new Date(contest.value.start_time!).getTime();
const endTime = new Date(contest.value.end_time!).getTime();
const progress = computed(() => {
  if (timestamp.value >= endTime) {
    return endTime - startTime;
  } else if (timestamp.value >= startTime) {
    return timestamp.value - startTime;
  } else {
    return 0;
  }
});
const percent = computed(() => {
  const sec = Math.round(progress.value / 1000);
  const p = +((100 * sec) / duration).toFixed(1);
  return Math.min(p, 100);
});
const formatProgress = (value: number) => {
  function alignNumber(value: number) {
    return (value < 10 ? '0' : '') + value;
  }
  value = duration * 1000 - value;
  const h = Math.floor(value / 3600000);
  const m = Math.floor((value % 3600000) / 60000);
  const s = Math.floor((value % 60000) / 1000);
  return `${h}:${alignNumber(m)}:${alignNumber(s)}`;
};
</script>

<template>
  <div flex gap8 lt-md:flex-col>
    <div flex-auto md:w="3/4">
      <slot></slot>
    </div>
    <div md:w="1/4" space-y-4>
      <div border="1 base" rounded-2>
        <h3 p4 border="b-1 base" font-bold>{{ contest.title }}</h3>
        <div p4>
          <div
            border="2 neutral-100 dark:gray-100"
            bg-neutral-100
            dark:bg-gray-100
            w-full
            h8
            rounded
            relative
          >
            <div
              h-full
              bg-success
              bg-op-100
              rounded
              :style="{
                width: percent + '%',
              }"
            ></div>
          </div>
        </div>
        <div px4 pb4 text-center text-lg font-600>
          <div v-if="isContestEnd(contest)">比赛已结束</div>
          <div v-else-if="isContestStart(contest)">
            <div>正在进行</div>
            <div>{{ formatProgress(progress) }}</div>
          </div>
          <div v-else>比赛即将开始</div>
        </div>
      </div>
      <div border="1 base" rounded-2>
        <h3 p4 border="b-1 base" font-bold>题目列表</h3>
        <div p4>
          <div v-for="problem in contest.problems">
            <nuxt-link
              :to="`/contest/${route.params.id}/problem/${displyaIdToIndex(
                problem.display_id
              )}`"
            >
              <span
                hover:text-gray-800
                :class="[
                  route.path.endsWith(
                    `/problem/${displyaIdToIndex(problem.display_id)}`
                  )
                    ? 'text-gray-800'
                    : 'text-gray-400',
                ]"
                >{{ displyaIdToIndex(problem.display_id) }}.
                {{ problem.title }}</span
              >
            </nuxt-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
