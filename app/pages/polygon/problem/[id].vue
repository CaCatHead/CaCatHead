<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const route = useRoute();

const { data } = await useFetchAPI<{ problem: FullPolygonProblem }>(
  `/api/polygon/${route.params.id}`
);

const problem = ref(data.value.problem);
</script>

<template>
  <div class="polygon-problem">
    <Head>
      <Title>Polygon #{{ problem.id }}. {{ problem.title }}</Title>
    </Head>
    <div>
      <h2 text-2xl font-bold mb4 px2>{{ problem.title }}</h2>
      <c-nav :prefix="`/polygon/problem/${route.params.id}/`" mb4>
        <c-nav-item to="">预览</c-nav-item>
        <c-nav-item to="edit">编辑题面</c-nav-item>
        <c-nav-item to="testcase">测试数据</c-nav-item>
        <c-nav-item to="permission">权限管理</c-nav-item>
      </c-nav>
      <NuxtPage :problem="problem" px2 />
    </div>
  </div>
</template>

<style>
.polygon-problem .c-nav-item {
  --at-apply: py2 px2 rounded text-sm;
  --at-apply: hover:bg-gray-200/50;
}
.polygon-problem .c-nav-item.active {
  --at-apply: bg-gray-200/50;
}
</style>
