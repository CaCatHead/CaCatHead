.,
<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const route = useRoute();

const notify = useNotification();

const { data } = await useFetchAPI<{ problem: FullPolygonProblem }>(
  `/api/polygon/${route.params.id}`
);

if (data.value === null) {
  await navigateTo('/polygon', { replace: true });
}

const problem = ref(data.value!.problem);

const user = useUser();

const files = ref<File[]>([]);

const getAxios = useAxiosFactory();
const loading = useLoadingIndicator();

const downloadZip = async () => {
  try {
    loading.start();
    const axios = await getAxios();
    const response = await axios.get(`/api/polygon/${route.params.id}/export`, {
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `form-data; filename="problem-${problem.value.display_id}.zip"`,
      },
      responseType: 'blob',
      onDownloadProgress(ev) {
        if (ev.progress) {
          loading.update(ev.progress * 100);
        } else {
          loading.update();
        }
      },
    });

    const data = window.URL.createObjectURL(response.data as Blob);
    const el = document.createElement('a');
    el.setAttribute('href', data);
    el.setAttribute('download', `${problem.value.title}.zip`);
    el.style.display = 'none';
    document.body.appendChild(el);
    el.click();
    document.body.removeChild(el);
  } finally {
    loading.stop();
  }
};

const onUpdateZip = async () => {
  if (files.value.length > 0) {
    const formData = new FormData();
    const file = files.value[0];
    formData.append('file', file);
    try {
      notify.success(
        `开始上传题目 #${problem.value.display_id}. ${problem.value.title} 压缩包`
      );

      loading.start();
      const axios = await getAxios();
      await axios.post(
        `/api/polygon/${problem.value.display_id}/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'application/zip',
            'Content-Disposition': `form-data; filename="problem-${problem.value.display_id}.zip"`,
          },
          onUploadProgress(ev) {
            if (ev.progress !== undefined) {
              loading.update(ev.progress * 100);
            } else {
              loading.update((ev.loaded / file.size) * 100.0);
            }
          },
        }
      );

      notify.success(
        `题目 #${problem.value.display_id}. ${problem.value.title} 更新成功`
      );
    } catch (err: unknown) {
      console.error(err);
      notify.danger(
        `题目 #${problem.value.display_id}. ${problem.value.title} 更新失败`
      );
    } finally {
      loading.stop();
    }
  }
};
</script>

<template>
  <div class="polygon-problem">
    <Head>
      <Title>Polygon #{{ problem.display_id }}. {{ problem.title }}</Title>
    </Head>

    <div>
      <div flex pl2 lt-md="flex-col mb4">
        <h2 text-2xl font-bold mb4>
          #{{ problem.display_id }}. {{ problem.title }}
        </h2>
        <div flex-auto></div>
        <div>
          <c-button mr2 variant="outline" color="info" @click="downloadZip"
            >下载题目包</c-button
          >
          <c-file-input
            id="update-zip"
            accept=".zip"
            v-model="files"
            @change="onUpdateZip"
            >上传题目包更新</c-file-input
          >
        </div>
      </div>
      <c-nav :prefix="`/polygon/problem/${route.params.id}/`" mb4 lt-md:pb2>
        <c-nav-item to="">预览</c-nav-item>
        <c-nav-item to="edit">编辑题面</c-nav-item>
        <c-nav-item to="testcase">测试数据</c-nav-item>
        <c-nav-item to="checker">Checker</c-nav-item>
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
