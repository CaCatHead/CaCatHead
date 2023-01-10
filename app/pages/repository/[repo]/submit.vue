<script setup lang="ts">
import type { ProblemRepository } from '@/composables/types';

const props = defineProps<{ repo: ProblemRepository }>();

const { repo } = toRefs(props);

useHead({
  title: `提交代码 - ${repo.value.name}`,
});

const notify = useNotification();

const route = useRoute();

const pid = ref(useRepoLastProblem(route.params.repo).value);

const submit = async (payload: { code: string; language: string }) => {
  const { code, language } = payload;
  try {
    await fetchAPI(
      `/api/repo/${route.params.repo}/problem/${pid.value}/submit`,
      {
        method: 'POST',
        body: {
          code,
          language,
        },
      }
    );
    notify.success('代码提交成功');
    await navigateTo(`/repository/${route.params.repo}/submissions`);
  } catch (error) {
    notify.danger('代码提交失败');
  }
};
</script>

<template>
  <div>
    <c-input type="number" id="pid" v-model="pid">
      <template #label>
        <span font-bold>题目编号</span>
      </template>
    </c-input>
    <problem-submit @submit="submit"></problem-submit>
  </div>
</template>
