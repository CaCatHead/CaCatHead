<script setup lang="ts">
import type { Contest } from '@/composables/types';

useHead({
  title: '比赛',
});

const user = useUser();

const { data } = await useFetchAPI<{ contests: Contest[] }>('/api/contests');
</script>

<template>
  <div>
    <c-table :data="data?.contests ?? []">
      <template #headers>
        <c-table-header name="title">比赛</c-table-header>
        <c-table-header name="start_time">比赛时间</c-table-header>
      </template>
      <template #title="{ row }">
        <nuxt-link :to="`/contest/${row.id}`" class="text-link">{{
          row.title
        }}</nuxt-link>
      </template>
      <template #start_time="{ row }">{{
        formatDateTime(row.start_time)
      }}</template>

      <template #empty>
        <div h="36" text-xl font-bold flex items-center justify-center>
          没有比赛
        </div>
      </template>
    </c-table>
    <div flex items-center v-if="user?.permissions.add_contest">
      <div></div>
      <div flex-auto></div>
      <div flex items-center>
        <c-button
          color="success"
          variant="outline"
          @click="navigateTo('/contests/new')"
          >新建比赛</c-button
        >
      </div>
    </div>
  </div>
</template>
