<script setup lang="ts">
import type { Post } from '@/composables/types';

const route = useRoute();
// const { data: post } = await useFetch<{ post: Post }>(
//   `/api/post/${route.params.id}`,
//   { baseURL: useRuntimeConfig().API_BASE }
// );
const { data: post } = await useFetchAPI<{ post: Post }>(
  `/api/post/${route.params.id}`
);
</script>

<template>
  <div>
    <Head>
      <Title>{{ post.post.title }}</Title>
    </Head>
    <h2 text-2xl font-bold>{{ post.post.title }}</h2>
    <p mt2 text-sm font-light>
      <span>用户 </span>
      <user-link :user="post.post.owner" />
      <span> 发表于 {{ formatDateTime(post.post.created) }}</span>
    </p>
    <div mt4 pl4 py2 border="l-4 base">{{ post.post.content }}</div>
  </div>
</template>
