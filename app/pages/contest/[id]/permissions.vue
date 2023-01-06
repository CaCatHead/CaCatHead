<script setup lang="ts">
import type { FullContest } from '@/composables/types';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `权限管理 - ${contest.value.title}`,
});
</script>

<template></template>
