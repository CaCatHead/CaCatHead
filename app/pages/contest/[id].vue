<script setup lang="ts">
import type {
  FullContest,
  Registration,
  ContestExtraInfo,
} from '@/composables/types';

const route = useRoute();

const { data: contest } = await useFetchAPI<{
  contest: FullContest;
  solved: Record<string, boolean>;
  registration: Registration | null;
  is_admin: boolean;
  extra_info: ContestExtraInfo | null;
}>(`/api/contest/${route.params.id}/content`);

const user = useUser();

if (
  contest !== undefined &&
  contest.value !== undefined &&
  contest.value !== null
) {
  useHead({
    title: `${contest.value?.contest.title}`,
  });
} else {
  await navigateTo(`/contests/register/${route.params.id}`, { replace: true });
}
</script>

<template>
  <div v-if="contest" class="c-contest">
    <h3 font-bold text-xl>{{ contest.contest.title }}</h3>
    <c-nav :prefix="`/contest/${route.params.id}/`" my4 lt-md="text-xs pb2">
      <c-nav-item to="">面板</c-nav-item>
      <c-nav-item to="submit" v-if="user">提交代码</c-nav-item>
      <c-nav-item to="status" v-if="user">我的提交</c-nav-item>
      <c-nav-item to="submissions" v-if="
        contest.is_admin ||
        (isContestEnd(contest.contest) &&
          contest.contest?.settings?.view_submissions_after_contest)
      ">所有提交</c-nav-item>
      <c-nav-item to="standings">排行榜</c-nav-item>
      <c-nav-item to="settings" v-if="contest.is_admin">比赛设置</c-nav-item>
      <c-nav-item to="problemset" v-if="contest.is_admin">题目列表设置</c-nav-item>
      <c-nav-item to="rating" v-if="isContestEnd(contest.contest)">Rating</c-nav-item>
      <c-nav-item to="permissions" v-if="contest.is_admin">权限管理</c-nav-item>
    </c-nav>
    <NuxtPage :contest="contest.contest" :solved="contest.solved" :registration="contest.registration"
      :admin="contest.is_admin" :extra_info="contest.extra_info" />
  </div>
</template>

<style>
.c-contest .c-nav-item {
  --at-apply: py2 px2 rounded text-sm;
  --at-apply: hover:bg-gray-200/50;
}

.c-contest .c-nav-item.active {
  --at-apply: bg-gray-200/50;
}
</style>
