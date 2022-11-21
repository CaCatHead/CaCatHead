<script setup lang="ts">
import type { Post } from '@/composables/types';

defineProps<{ posts: Post[] }>();
</script>

<template>
  <div>
    <div v-for="post in posts" mb12>
      <h2 text-2xl font-bold>
        <NuxtLink :to="`/post/entry/${post.id}`">{{ post.title }}</NuxtLink>
      </h2>
      <p mt2 text-sm font-light>
        <span>用户 </span>
        <user-link :user="post.owner" />
        <span>
          发表于<time-interval
            :left="post.created"
            :right="new Date()"
          ></time-interval
        ></span>
      </p>
      <p v-if="post.content" mt4 pl4 py2 border="l-4 base">
        {{ post.content }}
      </p>
      <div
        v-if="post.content"
        mt4
        px4
        py2
        border="1 base"
        rounded
        flex
        gap2
        text-sm
        font-light
      >
        <div flex-auto></div>
        <div>用户 <user-link :user="post.owner" /></div>
        <span>发表于 {{ formatDateTime(post.created) }}</span>
      </div>
    </div>
  </div>
</template>
