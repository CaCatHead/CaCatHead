<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const code = ref('');

const submit = async () => {
  const resp = await fetchAPI(`/api/polygon/${problem.value.id}/submit`, {
    method: 'POST',
    body: {
      language: 'cpp',
      code: code.value,
    },
  });
  console.log(resp);
  await navigateTo(`/polygon/problem/${problem.value.id}/status`);
};
</script>

<template>
  <div>
    <div>
      <span mr2 font-600>语言:</span>
      <span>C++</span>
    </div>
    <c-input type="textarea" id="code" v-model="code" font-mono>
      <template #label><span></span></template>
    </c-input>
    <div>
      <c-button color="success" w-full @click="submit">提交</c-button>
    </div>
  </div>
</template>
