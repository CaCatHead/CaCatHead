<script setup lang="ts">
import type { Post, Contest } from '@/composables/types';

useHead({
  title: '主页',
});

const { data } = await useFetchAPI<{ posts: Post[]; contests: Contest[] }>(
  `/api/home`
);

const posts = ref(data.value?.posts ?? []);
</script>

<template>
  <div flex gap8 lt-md:flex-col-reverse>
    <div w="5/8" lt-md:w-full>
      <PostList :posts="posts"></PostList>
    </div>
    <div w="3/8" lt-md:w-full space-y-8>
      <div shadow-box rounded>
        <h3 border="b-1 base" p4 text-xl font-bold>公告牌</h3>
        <div p4>
          <p>CaCatHead 是一个开源的在线评测系统，目前仍在开发过程中。</p>
          <p mt4>
            <nuxt-img src="/ccpc.png" alt="Cat CPC" preset="default" />
          </p>
        </div>
      </div>

      <div shadow-box rounded>
        <h3 border="b-1 base" p4 text-xl font-bold>最近比赛</h3>
        <div p4 text-sm>
          <c-table :data="data?.contests">
            <template #headers>
              <c-table-header name="title">比赛</c-table-header>
              <c-table-header name="start_time">开始时间</c-table-header>
            </template>
            <template #title="{ row }">
              <nuxt-link :to="`/contest/${row.id}`" text-link>{{
                row.title
              }}</nuxt-link>
            </template>
            <template #start_time="{ row }">
              <div text-xs>{{ formatDateTimeDay(row.start_time) }}</div>
              <div text-xs>{{ formatDateTimeTime(row.start_time) }}</div>
            </template>
          </c-table>
        </div>
      </div>
    </div>
  </div>
</template>
