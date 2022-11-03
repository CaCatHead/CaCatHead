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
    <div mt4>{{ post.post.content }}</div>
  </div>
</template>
