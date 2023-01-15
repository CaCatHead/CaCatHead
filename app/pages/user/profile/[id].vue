<script setup lang="ts">
import type { PublicUserProfile } from '@/composables/types';

import { format } from 'date-fns';

const route = useRoute();

const { data } = await useFetchAPI<{ user: PublicUserProfile }>(
  `/api/user/profile/${route.params.id}`
);

if (!data.value?.user) {
  await navigateTo('/');
}

useHead({
  title: `用户 ${data.value?.user.nickname}`,
});

const formatCNDateTime = (date: string | number | Date) =>
  format(new Date(date), 'yyyy 年 M 月 d 日');
</script>

<template>
  <div v-if="data?.user" space-y-4>
    <h3 font-bold text-3xl>{{ data.user.nickname }}</h3>
    <div text-sm text-base-500>
      注册于 {{ formatCNDateTime(data.user.joined) }}
    </div>
  </div>
</template>
