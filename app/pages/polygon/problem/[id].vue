<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const route = useRoute();

const { data } = await useFetchAPI<{ problem: FullPolygonProblem }>(
  `/api/polygon/${route.params.id}`
);
</script>

<template>
  <div>
    <Head>
      <Title>Polygon #{{ data.problem.id }}. {{ data.problem.title }}</Title>
    </Head>
    <NuxtPage :problem="data.problem" />
  </div>
</template>
