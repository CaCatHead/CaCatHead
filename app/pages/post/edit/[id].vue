<script setup lang="ts">
import type { Post } from '@/composables/types';

const route = useRoute();

const user = useUser();

const notify = useNotification();

const { data: post } = await useFetchAPI<{ post: Post }>(
  `/api/post/${route.params.id}`
);

if (!post.value) {
  await navigateTo('/posts', { replace: true });
}

useHead({
  title: '编辑博客',
});

const save = async () => {
  try {
    await fetchAPI(`/api/post/${route.params.id}/edit`, {
      method: 'POST',
      body: {
        title: post.value?.post.title,
        content: post.value?.post.content,
        is_home: post.value?.post.is_home,
        is_public: post.value?.post.is_public,
      },
    });

    notify.success(`公告 ${post.value?.post.title} 编辑成功`);
    await navigateTo(`/post/entry/${route.params.id}`);
  } catch {
    notify.danger(`公告 ${post.value?.post.title} 编辑失败`);
  }
};
</script>

<template>
  <div space-y-4 v-if="post?.post">
    <c-input type="text" id="title" v-model="post.post.title">
      <template #label><span font-bold>标题</span></template>
    </c-input>
    <markdown-editor v-model="post.post.content"></markdown-editor>
    <div v-if="user?.permissions.is_superuser" flex items-center space-x-4>
      <span font-bold>是否公开</span>
      <c-switch id="is_public" v-model="post.post.is_public"></c-switch>
    </div>
    <div v-if="user?.permissions.is_superuser" flex items-center space-x-4>
      <span font-bold>是否在首页</span>
      <c-switch id="is_home" v-model="post.post.is_home"></c-switch>
    </div>
    <div>
      <c-button color="success" @click="save">保存</c-button>
    </div>
  </div>
</template>
