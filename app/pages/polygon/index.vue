<script setup lang="ts">
import type { PolygonProblem } from '@/composables/types';

useHead({
  title: 'Polygon',
});

const { data, refresh } = await useFetchAPI<{ problems: PolygonProblem[] }>(
  `/api/polygon/own`,
  { initialCache: false }
);

if (!data.value?.problems) {
  await navigateTo('/');
}

const upload = async (ev: Event) => {
  const target = ev.target as HTMLInputElement;
  if ((target.files?.length ?? 0) === 0) {
    return;
  }
  const formData = new FormData();
  formData.append('file', target.files![0]);
  await fetchAPI(`/api/polygon/upload`, {
    method: 'POST',
    body: formData,
    headers: {
      'Content-Type': 'application/zip',
      'Content-Disposition': `form-data; filename="${target.files![0].name}"`,
    },
  });
  await refresh();
};
</script>

<template>
  <div>
    <div flex mb8 items-center>
      <div>
        <h2 text-2xl font-bold mb4>Polygon</h2>
        <h3 text-lg font-500>程序设计竞赛试题创建系统</h3>
      </div>
      <div flex-auto></div>
      <div flex items-center>
        <c-button
          color="success"
          mr4
          variant="outline"
          @click="navigateTo('/polygon/new')"
          >新建题目</c-button
        >
        <c-file-input
          id="upload-problem"
          color="success"
          accept=".zip"
          @change="upload"
          >上传题目</c-file-input
        >
      </div>
    </div>

    <c-table :data="data!.problems">
      <template #headers>
        <c-table-header
          name="id"
          label="#"
          width="64px"
          row-class="text-center font-600"
        ></c-table-header>
        <c-table-header
          name="title"
          label="标题"
          class="text-left"
          align="left"
        ></c-table-header>
        <c-table-header
          name="owner"
          label="创建者"
          row-class="text-center"
        ></c-table-header>
      </template>

      <template #title="{ row }">
        <nuxt-link
          :to="`/polygon/problem/${row.id}/`"
          text-sky-700
          text-op-80
          hover:text-op-100
          >{{ row.title }}</nuxt-link
        >
      </template>
      <template #owner="{ row }">
        <user-link :user="row.owner"></user-link>
      </template>
    </c-table>
  </div>
</template>
