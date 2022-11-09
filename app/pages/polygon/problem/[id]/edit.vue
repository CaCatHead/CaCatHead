<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const submit = async () => {
  await fetchAPI(`/api/polygon/${problem.value.id}/edit`, {
    method: 'POST',
    body: {
      title: problem.value.title,
      description: problem.value.problem_info.problem_content.description,
      input: problem.value.problem_info.problem_content.input,
      output: problem.value.problem_info.problem_content.output,
      hint: problem.value.problem_info.problem_content.hint,
    },
  });

  await navigateTo(`/polygon/problem/${problem.value.id}/`);
};
</script>

<template>
  <div>
    <div space-y-4>
      <c-input
        id="title"
        name="标题"
        type="text"
        v-model="problem.title"
      ></c-input>

      <c-input
        id="description"
        name="题目描述"
        type="textarea"
        v-model="problem.problem_info.problem_content.description"
      ></c-input>

      <c-input
        id="input"
        name="输入格式"
        type="textarea"
        v-model="problem.problem_info.problem_content.input"
      ></c-input>

      <c-input
        id="output"
        name="输出格式"
        type="textarea"
        v-model="problem.problem_info.problem_content.output"
      ></c-input>

      <c-input
        id="hint"
        name="提示"
        type="textarea"
        v-model="problem.problem_info.problem_content.hint"
      ></c-input>
    </div>
    <div>
      <c-button color="success" @click="submit">保存</c-button>
    </div>
  </div>
</template>
