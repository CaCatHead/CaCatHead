<script setup lang="ts">
import type { ProblemRepository } from '@/composables/types';

const props = defineProps<{ repo: ProblemRepository }>();

const { repo } = toRefs(props);

useHead({
  title: `提交代码 - ${repo.value.name}`,
});

const pid = ref(1000);

const route = useRoute();
</script>

<template>
  <div>
    <c-input type="number" id="pid" v-model="pid">
      <template #label>
        <span font-bold>题目编号</span>
      </template>
    </c-input>
    <problem-submit></problem-submit>
  </div>
</template>
