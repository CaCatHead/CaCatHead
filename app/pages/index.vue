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
      <div v-for="post in posts" mb12>
        <h2 text-2xl font-bold>
          <NuxtLink :to="`/post/${post.id}`">{{ post.title }}</NuxtLink>
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
        <p mt4 pl4 py2 border="l-4 base">{{ post.content }}</p>
        <div mt4 px4 py2 border="1 base" rounded flex gap2 text-sm font-light>
          <div flex-auto></div>
          <div>用户 <user-link :user="post.owner" /></div>
          <span>发表于 {{ formatDateTime(post.created) }}</span>
        </div>
      </div>
    </div>
    <div w="3/8" lt-md:w-full>
      <div shadow-box rounded>
        <h3 border="b-1 base" p4 text-xl font-bold>公告牌</h3>
        <div p4>
          <p>CaCatHead 是一个开源的在线评测系统，目前仍在开发过程中。</p>
          <p mt4>
            <img src="/ccpc.png" alt="" srcset="" />
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
