<script setup lang="ts">
import type { FullContest } from '@/composables/types';

const route = useRoute();
const user = useUser();
const notify = useNotification();

const { data: contest } = await useFetchAPI<{
  contest: FullContest;
  is_admin: boolean;
}>(`/api/contest/${route.params.id}/content`);

if (
  contest !== undefined &&
  contest.value !== undefined &&
  contest.value !== null
) {
  useHead({
    title: `${contest.value?.contest.title}`,
  });
} else {
  notify.danger('比赛未找到或你无权访问此比赛');
  await navigateTo('/contests');
}
</script>

<template>
  <div v-if="contest" class="c-contest">
    <h3 font-bold text-xl>{{ contest.contest.title }}</h3>
    <c-nav :prefix="`/contest/${route.params.id}/`" my4 lt-md="text-xs">
      <c-nav-item to="">面板</c-nav-item>
      <c-nav-item to="submit">提交代码</c-nav-item>
      <c-nav-item to="status">我的提交</c-nav-item>
      <c-nav-item
        to="submissions"
        v-if="
          contest.is_admin ||
          (isContestEnd(contest.contest) &&
            contest.contest?.settings?.view_submissions_after_contest)
        "
        >所有提交</c-nav-item
      >
      <c-nav-item to="standings">排行榜</c-nav-item>
      <c-nav-item to="settings" v-if="contest.is_admin">比赛设置</c-nav-item>
      <c-nav-item to="permissions" v-if="contest.is_admin">权限管理</c-nav-item>
    </c-nav>
    <NuxtPage :contest="contest.contest" :admin="contest.is_admin" />
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
