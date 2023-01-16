<script setup lang="ts">
import type { ProblemRepository } from '@/composables/types';

const route = useRoute();

const user = useUser();

const { data } = await useFetchAPI<{
  repo: ProblemRepository;
}>(`/api/repo/${route.params.repo}`);

const repo = computed(() => data.value?.repo);

if (!repo.value) {
  await navigateTo(`/repository/1`);
}

useHead({
  title: `${repo.value?.name}`,
});
</script>

<template>
  <div v-if="repo" class="c-repo">
    <h3 font-bold text-xl>{{ repo.name }}</h3>
    <c-nav
      :prefix="`/repository/${route.params.repo}/`"
      my4
      lt-md="text-xs pb2"
    >
      <c-nav-item to="">题目集</c-nav-item>
      <c-nav-item to="submit">提交代码</c-nav-item>
      <!-- <c-nav-item to="status">我的提交</c-nav-item> -->
      <c-nav-item to="submissions">所有提交</c-nav-item>
      <c-nav-item
        to="settings"
        v-if="user?.permissions.is_staff || user?.permissions.is_superuser"
        >题库设置</c-nav-item
      >
      <c-nav-item
        to="problemset"
        v-if="user?.permissions.is_staff || user?.permissions.is_superuser"
        >题目列表设置</c-nav-item
      >
    </c-nav>
    <NuxtPage :repo="repo" />
  </div>
</template>

<style>
.c-repo .c-nav-item {
  --at-apply: py2 px2 rounded text-sm;
  --at-apply: hover:bg-gray-200/50;
}
.c-repo .c-nav-item.active {
  --at-apply: bg-gray-200/50;
}
</style>
