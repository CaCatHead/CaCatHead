<script setup lang="ts">
import type { Contest, Registration } from '@/composables/types';

const notify = useNotification();

const route = useRoute();

const { data: contest } = await useFetchAPI<{
  contest: Contest;
  registration: Registration | null;
}>(`/api/contest/${route.params.id}/public`);

if (!contest.value) {
  notify.danger('比赛未找到或你无权访问此比赛');
  await navigateTo(`/contests`, { replace: true });
} else if (isContestEnd(contest.value.contest)) {
  notify.danger(`比赛 ${contest.value?.contest.title} 已经结束`);
  await navigateTo(`/contest/${route.params.id}`, { replace: true });
}

useHead({
  title: `注册比赛 ${contest.value?.contest.title}`,
});

const user = useUser();
if (!user || !user.value) {
  await navigateTo({
    path: '/login',
    query: {
      redirect: route.fullPath,
    },
  });
}

const name = ref(
  contest.value?.registration?.name ??
    user?.value?.nickname ??
    user?.value?.username ??
    ''
);

const register = async () => {
  try {
    await fetchAPI(`/api/contest/${route.params.id}/register`, {
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

const unregister = async () => {
  try {
    await fetchAPI(`/api/contest/${route.params.id}/unregister`, {
      method: 'POST',
    });
    notify.success(`比赛 ${contest.value?.contest.title} 取消注册成功`);
    await navigateTo(`/contests`);
  } catch {
    notify.danger(`比赛 ${contest.value?.contest.title} 取消注册失败`);
  }
};
</script>

<template>
  <div space-y-4>
    <h3 text-2xl font-bold>注册比赛 {{ contest?.contest.title }}</h3>
    <c-input type="text" id="team_name" v-model="name">
      <template #label>队伍名称</template>
    </c-input>
    <div v-if="!contest?.registration">
      <c-button w-full color="success" @click="register">注册</c-button>
    </div>
    <div v-else space-y-4>
      <div border rounded p4 bg-success bg-op-30 font-bold>
        你已经注册本比赛
      </div>
      <div flex gap4>
        <c-button w="1/2" color="success" @click="register">更新信息</c-button>
        <c-button w="1/2" color="danger" @click="unregister">取消注册</c-button>
      </div>
    </div>
  </div>
</template>
