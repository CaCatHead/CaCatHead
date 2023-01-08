<script setup lang="ts">
import type { PolygonProblem } from '@/composables/types';

useHead({
  title: 'Polygon',
});

const notify = useNotification();

const { data, refresh } = await useFetchAPI<{ problems: PolygonProblem[] }>(
  `/api/polygon/own`
);

if (!data.value?.problems) {
  await navigateTo('/');
}

const files = ref<File[]>([]);
const upload = async () => {
  if (files.value.length > 0) {
    const file = files.value[0];
    const formData = new FormData();
    formData.append('file', file);
    try {
      await fetchAPI(`/api/polygon/upload`, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/zip',
          'Content-Disposition': `form-data; filename="${encodeURIComponent(
            file.name
          )}"`,
        },
      });
      await refresh();
    } catch (err: unknown) {
      console.error(err);
      notify.danger(`题目上传失败`);
    }
  }
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
          v-model="files"
          @change="upload"
          >上传题目</c-file-input
        >
      </div>
    </div>

    <c-table :data="data?.problems ?? []">
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
        <c-table-header name="updated" label="更新时间"></c-table-header>
      </template>

      <template #updated="{ row }">
        <div>{{ formatDateTime(row.updated) }}</div>
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
