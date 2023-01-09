<script setup lang="ts">
import type { JudgeNode } from '@/composables/types';

useHead({
  title: '评测机',
});

const { data } = await useFetchAPI<{ nodes: JudgeNode[] }>(`/api/judge/nodes`);
</script>

<template>
  <div space-y-4>
    <h2 font-bold text-2xl flex items-center gap2>
      <span i-carbon-bare-metal-server text-3xl></span>
      <span>评测机</span>
    </h2>
    <div v-if="data?.nodes">
      <judge-nodes :nodes="data?.nodes"></judge-nodes>
    </div>
  </div>
</template>
