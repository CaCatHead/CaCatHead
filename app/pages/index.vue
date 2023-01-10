<script setup lang="ts">
import type { Post } from '@/composables/types';

useHead({
  title: '主页',
});

const { data } = await useFetchAPI<{ posts: Post[] }>('/api/posts/public');

const posts = ref(data.value?.posts ?? []);
</script>

<template>
  <div flex gap8 lt-md:flex-col-reverse>
    <div w="5/8" lt-md:w-full>
      <PostList :posts="posts"></PostList>
    </div>
    <div w="3/8" lt-md:w-full>
      <div shadow-box rounded>
        <h3 border="b-1 base" p4 text-xl font-bold>公告牌</h3>
        <div p4>
          <p>CaCatHead 是一个开源的在线评测系统，目前仍在开发过程中。</p>
          <p mt4>
            <nuxt-img src="/ccpc.png" alt="Cat CPC" format="webp" />
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
