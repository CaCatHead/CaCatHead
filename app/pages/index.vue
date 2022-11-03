<script setup lang="ts">
useHead({
  title: '主页',
});

const { data } = await useFetchAPI<{ posts: any[] }>('/api/posts/public');
</script>

<template>
  <div>
    <div v-for="post in data.posts" mb8>
      <h2 text-2xl>
        <NuxtLink :to="`/post/${post.id}`">{{ post.title }}</NuxtLink>
      </h2>
      <p mt2 text-sm font-light>
        <span>用户 </span>
        <user-link :user="post.owner" />
        <span> 发表于 {{ formatDateTime(post.created) }}</span>
      </p>
      <p mt2>{{ post.content }}</p>
    </div>
  </div>
</template>
