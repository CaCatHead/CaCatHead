<script setup lang="ts">
import type { Contest } from '@/composables/types';

useHead({
  title: '比赛',
});

const user = useUser();

const notify = useNotification();

const timestamp = useServerTimestamp();

const { data } = await useFetchAPI<{ contests: Contest[] }>('/api/contests');

const now = timestamp.value;
const currentContests = computed(() => {
  return (
    data.value?.contests.filter(c => new Date(c.end_time).getTime() >= now) ??
    []
  );
});
const upcomingContest = computed(() => {
  for (const contest of currentContests.value) {
    const start = new Date(contest.start_time).getTime();
    if (now <= start && start <= now + 15 * 60 * 1000) {
      console.log(contest);
      return contest;
    }
  }
});
const upcomingContestStartTime = computed(() => {
  if (upcomingContest.value) {
    return new Date(upcomingContest.value.start_time).getTime();
  } else {
    return Number.MAX_SAFE_INTEGER;
  }
});

const openHistory = ref(!upcomingContest.value);
const historyContests = computed(() => {
  return (
    data.value?.contests.filter(c => new Date(c.end_time).getTime() < now) ?? []
  );
});

if (currentContests.value.length > 0) {
  let jumped = false;
  watch(timestamp, async timestamp => {
    if (jumped) return;
    for (const contest of currentContests.value) {
      const start = new Date(contest.start_time).getTime();
      if (start <= timestamp && timestamp <= start + 1000) {
        notify.success(`比赛 ${contest.title} 开始...`);
        jumped = true;
        await navigateTo(`/contest/${contest.id}`);
        break;
      }
    }
  });
}

const contestStatus = (contest: Contest) => {
  const now = new Date(timestamp.value);
  const start_time = new Date(contest.start_time);
  const end_time = new Date(contest.end_time);
  if (now.getTime() >= end_time.getTime()) {
    return '已结束';
  } else if (now.getTime() >= start_time.getTime()) {
    return '正在进行';
  } else {
    return '即将开始';
  }
};
const statusColor = (status: string) => {
  if (status === '已结束') {
    return 'text-danger';
  } else if (status === '正在进行') {
    return 'text-success';
  } else {
    return 'text-info';
  }
};

const formatProgress = (value: number) => {
  function alignNumber(value: number) {
    return (value < 10 ? '0' : '') + value;
  }
  const h = Math.floor(value / 3600000);
  const m = Math.floor((value % 3600000) / 60000);
  const s = Math.floor((value % 60000) / 1000);
  return `${h}:${alignNumber(m)}:${alignNumber(s)}`;
};
</script>

<template>
  <div space-y-4>
    <div flex items-center justify-between lt-sm="flex-col gap2 items-start">
      <h3 font-bold text-xl>正在进行或即将开始的比赛</h3>
      <div v-if="user?.permissions.add_contest">
        <c-button
          color="success"
          variant="outline"
          @click="navigateTo('/contests/new')"
          >新建比赛</c-button
        >
      </div>
    </div>
    <c-table
      :data="
        openHistory && upcomingContest ? [upcomingContest!] : currentContests
      "
      border
    >
      <template #headers>
        <c-table-header name="title">比赛</c-table-header>
        <c-table-header name="start_time">开始时间</c-table-header>
        <c-table-header name="duration" width="160">持续时间</c-table-header>
        <c-table-header name="status" width="120">公开 / 状态</c-table-header>
        <c-table-header name="operation"><span></span></c-table-header>
      </template>
      <template #title="{ row }">
        <div
          v-if="contestStatus(row) === '即将开始' && !isContestAdmin(row, user)"
        >
          <nuxt-link :to="`/contests/register/${row.id}`" class="text-link">{{
            row.title
          }}</nuxt-link>
        </div>
        <div v-else>
          <nuxt-link :to="`/contest/${row.id}`" class="text-link">{{
            row.title
          }}</nuxt-link>
        </div>
      </template>
      <template #start_time="{ row }">
        <div>
          <span>{{ formatDateTime(row.start_time) }}</span>
        </div>
      </template>
      <template #duration="{ row }">
        <span>{{ formatContestDuration(row) }}</span>
      </template>
      <template #status="{ row, smallScreen }">
        <div
          flex
          items-center
          gap2
          :class="smallScreen ? 'justify-end' : 'justify-center'"
        >
          <span block>
            <span
              v-if="row.is_public"
              class="block i-mdi-check text-success text-xl"
            ></span>
            <span
              v-else="row.is_public"
              class="block i-mdi-close text-danger text-xl"
            ></span>
          </span>
          <span :class="[statusColor(contestStatus(row))]">{{
            contestStatus(row)
          }}</span>
        </div>
      </template>
      <template #operation="{ row }">
        <div inline-flex lt-md:mr="-4">
          <c-button
            variant="text"
            color="success"
            @click="navigateTo(`/contests/register/${row.id}`)"
            >注册</c-button
          >
          <c-button
            v-if="contestStatus(row) === '正在进行'"
            variant="text"
            color="info"
            @click="navigateTo(`/contest/${row.id}`)"
            >进入比赛</c-button
          >
        </div>
      </template>

      <template #empty>
        <div h="36" text-xl font-bold flex items-center justify-center>
          没有比赛
        </div>
      </template>
    </c-table>

    <client-only>
      <div v-if="upcomingContest" text-right text-base-500 class="!mt1">
        <span
          text-sm
          select-none
          cursor-pointer
          text-link
          @click="openHistory = !openHistory"
          >{{ openHistory ? '隐藏' : '显示' }}比赛历史</span
        >
      </div>
      <div v-if="upcomingContest" space-y-2 pt-12>
        <h3 font-bold text-3xl text-center>
          <nuxt-link :to="`/contest/${upcomingContest.id}`">{{
            upcomingContest.title
          }}</nuxt-link>
        </h3>
        <div
          text-base-500
          text-center
          flex
          flex-col
          items-center
          justify-center
          h48
        >
          <div mb2>距离比赛开始还有</div>
          <div text-2xl>
            <span>{{
              formatProgress(Math.max(0, upcomingContestStartTime - timestamp))
            }}</span>
          </div>
        </div>
      </div>
    </client-only>

    <div>
      <display-server-timestamp justify-end></display-server-timestamp>
      <client-only> </client-only>
    </div>

    <h3 v-show="openHistory" font-bold text-xl>比赛历史</h3>
    <c-table v-show="openHistory" :data="historyContests" border>
      <template #headers>
        <c-table-header name="title">比赛</c-table-header>
        <c-table-header name="start_time">开始时间</c-table-header>
        <c-table-header name="duration">持续时间</c-table-header>
      </template>
      <template #title="{ row }">
        <nuxt-link :to="`/contest/${row.id}`" class="text-link">{{
          row.title
        }}</nuxt-link>
      </template>
      <template #start_time="{ row }">{{
        formatDateTime(row.start_time)
      }}</template>
      <template #duration="{ row }">
        {{ formatContestDuration(row) }}
      </template>

      <template #empty>
        <div h="36" text-xl font-bold flex items-center justify-center>
          没有比赛
        </div>
      </template>
    </c-table>

    <div flex items-center v-if="user?.permissions.add_contest">
      <div></div>
      <div flex-auto></div>
      <div flex items-center></div>
    </div>
  </div>
</template>
