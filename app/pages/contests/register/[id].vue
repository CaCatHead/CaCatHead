<script setup lang="ts">
import type { Contest, Registration } from '@/composables/types';

const route = useRoute();

const { data: contest } = await useFetchAPI<{
  contest: Contest;
  registration: Registration | null;
}>(`/api/contest/${route.params.id}/public`);

useHead({
  title: `注册比赛 ${contest.value?.contest.title}`,
});

const notify = useNotification();
const user = useUser();
console.log(user?.value);
if (!user || !user.value) {
  await navigateTo('/login');
}

const name = ref(
  contest.value?.registration?.name ??
    user?.value?.nickname ??
    user?.value?.username ??
    ''
);

const submit = async () => {
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
</script>

<template>
  <div space-y-4>
    <h3 text-2xl font-bold>注册比赛 {{ contest?.contest.title }}</h3>
    <c-input type="text" id="team_name" v-model="name">
      <template #label>队伍名称</template>
    </c-input>
    <div v-if="!contest?.registration">
      <c-button w-full color="success" @click="submit">注册</c-button>
    </div>
    <div v-else space-y-4>
      <div border rounded p4 bg-success bg-op-30 font-bold>
        你已经注册本比赛
      </div>
      <div flex gap4>
        <c-button w="1/2" color="success" @click="submit">更新信息</c-button>
        <c-button w="1/2" color="danger">取消注册</c-button>
      </div>
    </div>
  </div>
</template>
