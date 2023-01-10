<script setup lang="ts">
import type { ProblemRepository } from '@/composables/types';

const props = defineProps<{ repo: ProblemRepository }>();

const { repo } = toRefs(props);

useHead({
  title: `提交代码 - ${repo.value.name}`,
});

const route = useRoute();
</script>

<template></template>
