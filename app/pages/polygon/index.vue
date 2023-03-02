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
  await navigateTo('/', { replace: true });
}

type Tag = 'like' | 'archive' | 'none';
const tags = useLocalStorage(
  'polygon/problems/tags',
  ref<Record<string, Tag>>({})
);

const getTag = (p: PolygonProblem) => {
  if (p.id in tags.value) {
    return tags.value?.[p.id] ?? 'none';
  } else {
    return 'none';
  }
};
const toggleLike = (p: PolygonProblem) => {
  if (tags.value) {
    const tag = getTag(p);
    if (tag === 'like') {
      tags.value[p.id] = 'none';
    } else {
      tags.value[p.id] = 'like';
    }
  }
};

const prolems = computed(() => {
  const problems = data.value?.problems ?? [];
  return problems.sort((l, r) => {
    const lt = getTag(l);
    const rt = getTag(r);
    if (lt == rt) {
      return r.id - l.id;
    } else {
      return lt.localeCompare(rt);
    }
  });
});

const files = ref<File[]>([]);

const getAxios = useAxiosFactory();
const loading = useLoadingIndicator();

const upload = async () => {
  if (files.value.length > 0) {
    loading.start();
    const axios = await getAxios();
    const file = files.value[0];
    const formData = new FormData();
    formData.append('file', file);
    try {
      await axios.post(`/api/polygon/upload`, formData, {
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
    } finally {
      loading.stop();
    }
  }
};
</script>

<template>
  <div>
    <div flex mb8 items-center lt-md="flex-col items-start gap2">
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

    <c-table :data="prolems">
      <template #headers>
        <c-table-header
          name="display_id"
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
        <c-table-header
          name="updated"
          label="更新时间"
          width="200px"
        ></c-table-header>
        <c-table-header name="operation" label="" width="60px"></c-table-header>
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
      <template #operation="{ row }">
        <c-button
          color="warning"
          variant="text"
          :icon="
            getTag(row) === 'like' ? 'i-carbon-star-filled' : 'i-carbon-star'
          "
          @click="toggleLike(row)"
        ></c-button>
      </template>
    </c-table>
  </div>
</template>
