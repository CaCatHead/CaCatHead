<script setup lang="ts">
import type { Post } from '@/composables/types';

useHead({
  title: '博客',
});

const { data } = await useFetchAPI<{ posts: Post[] }>('/api/posts');
</script>

<template>
  <div>
    <PostList :posts="data.posts"></PostList>
  </div>
</template>
