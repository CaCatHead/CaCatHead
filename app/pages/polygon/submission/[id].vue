<script setup lang="ts">
const route = useRoute();

const { data } = await useFetchAPI<{ submission: any }>(
  `/api/polygon/submission/${route.params.id}`
);

if (data.value === null) {
  await navigateTo(`/polygon`);
}

const submission = ref(data.value!.submission);
</script>

<template>
  <div>
    <div>结果: {{ submission.verdict }}</div>
    <div>得分: {{ submission.score }}</div>
    <div font-mono p4 shadow-box>{{ submission.code }}</div>
  </div>
</template>
