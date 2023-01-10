<script setup lang="ts">
import type { Contest } from '@/composables/types';

useHead({
  title: '创建比赛',
});

const title = ref('');

const submit = async () => {
  const { contest } = await fetchAPI<{ contest: Contest }>(`/api/contest`, {
    method: 'POST',
    body: { title: title.value ?? 'Unknown', type: 'icpc' },
  });
  await navigateTo(`/contest/${contest.id}`);
};
</script>

<template>
  <div>
    <div flex mb8 items-center>
      <div>
        <h2 text-2xl font-bold mb4>创建新的比赛</h2>
      </div>
    </div>
    <div mb8>
      <c-input
        mt4
        id="title"
        name="标题"
        type="text"
        color="success"
        v-model="title"
      >
      </c-input>
    </div>
    <div>
      <c-button color="success" @click="submit">创建</c-button>
    </div>
  </div>
</template>
