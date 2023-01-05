<script setup lang="ts">
import type { FullContest } from '@/composables/types';

const route = useRoute();
const user = useUser();
const notify = useNotification();

const { data: contest } = await useFetchAPI<{ contest: FullContest }>(
  `/api/contest/${route.params.id}/content`
);

if (
  contest !== undefined &&
  contest.value !== undefined &&
  contest.value !== null
) {
  useHead({
    title: `比赛 ${contest.value?.contest.title}`,
  });
} else {
  notify.danger('比赛未找到或你无权访问此比赛');
  await navigateTo('/contests');
}
</script>

<template>
  <div v-if="contest" class="c-contest">
    <h3 font-bold text-xl>{{ contest.contest.title }}</h3>
    <c-nav :prefix="`/contest/${route.params.id}/`" my4>
      <c-nav-item to="">面板</c-nav-item>
      <c-nav-item to="submit">提交代码</c-nav-item>
      <c-nav-item to="status">我的提交</c-nav-item>
      <c-nav-item
        to="submissions"
        v-if="
          isContestAdmin(contest.contest, user) ||
          (isContestEnd(contest.contest) &&
            contest.contest?.settings?.view_submissions_after_contest)
        "
        >所有提交</c-nav-item
      >
      <c-nav-item to="standings">排行榜</c-nav-item>
      <c-nav-item to="settings" v-if="isContestAdmin(contest.contest, user)"
        >比赛设置</c-nav-item
      >
      <c-nav-item to="permissions" v-if="isContestAdmin(contest.contest, user)"
        >权限管理</c-nav-item
      >
    </c-nav>
    <NuxtPage :contest="contest.contest" />
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
