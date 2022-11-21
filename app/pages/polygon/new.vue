<script setup lang="ts">
import type { PolygonProblem } from '@/composables/types';

const title = ref('');

const submit = async () => {
  const { problem } = await fetchAPI<{ problem: PolygonProblem }>(
    `/api/polygon/create`,
    {
      method: 'POST',
      body: { title: title.value ?? 'Unknown' },
    }
  );
  await navigateTo(`/polygon/problem/${problem.id}`);
};
</script>

<template>
  <div>
    <div flex mb8 items-center>
      <div>
        <h2 text-2xl font-bold mb4>创建新的题目</h2>
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
