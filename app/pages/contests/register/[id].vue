<script setup lang="ts">
import type { Contest } from '@/composables/types';

const route = useRoute();

const { data: contest } = await useFetchAPI<{ contest: Contest }>(
  `/api/contest/${route.params.id}/public`
);

useHead({
  title: `注册比赛 ${contest.value?.contest.title}`,
});

const notify = useNotification();
const user = useUser();

if (!user) {
  await navigateTo('/login');
}

const name = ref(user?.value?.nickname ?? user?.value?.username ?? '');

const submit = async () => {
  try {
    await fetchAPI(`/contest/${route.params.id}/register`, {
      method: 'POST',
      body: {
        name: name.value,
        extra_info: {},
      },
    });
    notify.success(`比赛 ${contest.value?.contest.title} 注册成功`);
    await navigateTo(`/contests`);
  } catch {
    notify.danger(`比赛 ${contest.value?.contest.title} 注册失败`);
  }
};
</script>

<template>
  <div space-y-4>
    <h3 text-2xl font-bold>注册比赛 {{ contest?.contest.title }}</h3>
    <c-input type="text" id="team_name" v-model="name">
      <template #label>队伍名称</template>
    </c-input>
    <c-button w-full color="success" @click="submit">注册</c-button>
  </div>
</template>
