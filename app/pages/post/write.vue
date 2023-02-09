<script setup lang="ts">
import type { Post } from '@/composables/types';

const user = useUser();

const notify = useNotification();

useHead({
  title: '创建博客',
});

const title = ref('');
const content = ref('');
const is_public = ref(false);

const save = async () => {
  if (!title.value || !content.value) {
    return;
  }

  try {
    const data = await fetchAPI<{ post: Post }>(`/api/post`, {
      method: 'POST',
      body: {
        title: title.value,
        content: content.value,
        sort_time: new Date().toISOString(),
        is_public: is_public.value,
        is_home: false,
      },
    });

    notify.success(`公告 ${title.value} 发布成功`);
    await navigateTo(`/post/entry/${data.post.id}`);
  } catch {
    notify.danger(`公告 ${title.value} 发布失败`);
  }
};
</script>

<template>
  <div space-y-4>
    <c-input type="text" id="title" v-model="title">
      <template #label><span font-bold>标题</span></template>
    </c-input>
    <markdown-editor v-model="content"></markdown-editor>
    <div v-if="user?.permissions.is_superuser" flex items-center space-x-4>
      <span font-bold>是否公开</span>
      <c-switch id="is_public" v-model="is_public"></c-switch>
    </div>
    <div>
      <c-button color="success" @click="save">保存</c-button>
    </div>
  </div>
</template>
