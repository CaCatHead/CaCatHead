<script setup lang="ts">
import type { Contest } from '@/composables/types';

useHead({
  title: '比赛',
});

const user = useUser();

const { data } = await useFetchAPI<{ contests: Contest[] }>('/api/contests');

const now = new Date().getTime();
const currentContests = computed(() => {
  return data.value?.contests.filter(
    c => new Date(c.end_time).getTime() >= now
  );
});
const historyContests = computed(() => {
  return data.value?.contests.filter(c => new Date(c.end_time).getTime() < now);
});

const contestStatus = (contest: Contest) => {
  const now = new Date();
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
</script>

<template>
  <div space-y-4>
    <h3 font-bold text-xl>正在进行或即将开始的比赛</h3>
    <c-table :data="currentContests">
      <template #headers>
        <c-table-header name="title">比赛</c-table-header>
        <c-table-header name="start_time">开始时间</c-table-header>
        <c-table-header name="duration" width="160">持续时间</c-table-header>
        <c-table-header name="status" width="120">权限 / 状态</c-table-header>
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

    <h3 font-bold text-xl>比赛历史</h3>
    <c-table :data="historyContests">
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
      <div flex items-center>
        <c-button
          color="success"
          variant="outline"
          @click="navigateTo('/contests/new')"
          >新建比赛</c-button
        >
      </div>
    </div>
  </div>
</template>
