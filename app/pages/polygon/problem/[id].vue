<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const route = useRoute();

const notify = useNotification();

const { data } = await useFetchAPI<{ problem: FullPolygonProblem }>(
  `/api/polygon/${route.params.id}`
);

if (data.value === null) {
  await navigateTo('/polygon');
}

const problem = ref(data.value!.problem);

const user = useUser();

const files = ref<File[]>([]);

const onUpdateZip = async () => {
  if (files.value.length > 0) {
    const formData = new FormData();
    const file = files.value[0];
    formData.append('file', file);
    try {
      await fetchAPI(`/api/polygon/${problem.value.id}/upload`, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/zip',
          'Content-Disposition': `form-data; filename="${file.name}"`,
        },
      });
      notify.success(`题目 ${problem.value.title} 更新成功`);
    } catch {
      notify.danger(`题目 ${problem.value.title} 更新失败`);
    }
  }
};
</script>

<template>
  <div class="polygon-problem">
    <Head>
      <Title>Polygon #{{ problem.id }}. {{ problem.title }}</Title>
    </Head>
    <div>
      <div flex pl2>
        <h2 text-2xl font-bold mb4>{{ problem.title }}</h2>
        <div flex-auto></div>
        <div>
          <c-file-input
            id="update-zip"
            accept=".zip"
            v-model="files"
            @change="onUpdateZip"
            >上传题目包更新</c-file-input
          >
        </div>
      </div>
      <c-nav :prefix="`/polygon/problem/${route.params.id}/`" mb4>
        <c-nav-item to="">预览</c-nav-item>
        <c-nav-item to="edit">编辑题面</c-nav-item>
        <c-nav-item to="testcase">测试数据</c-nav-item>
        <c-nav-item to="submit">提交代码</c-nav-item>
        <c-nav-item to="status">所有提交</c-nav-item>
        <c-nav-item to="permission" v-if="problem.owner.id === user?.id"
          >权限管理</c-nav-item
        >
      </c-nav>
      <NuxtPage :problem="problem" pl2 />
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
