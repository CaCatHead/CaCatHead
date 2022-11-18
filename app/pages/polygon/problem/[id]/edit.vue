<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const notify = useNotification();

const submit = async () => {
  await fetchAPI(`/api/polygon/${problem.value.id}/edit`, {
    method: 'POST',
    body: {
      title: problem.value.title,
      description: problem.value.problem_info.problem_content.description ?? '',
      input: problem.value.problem_info.problem_content.input ?? '',
      output: problem.value.problem_info.problem_content.output ?? '',
      hint: problem.value.problem_info.problem_content.hint ?? '',
    },
  });

  notify.success(`题目 ${problem.value.title} 修改成功`);
  await navigateTo(`/polygon/problem/${problem.value.id}/`);
};
</script>

<template>
  <div>
    <div space-y-8>
      <c-input id="title" type="text" v-model="problem.title">
        <template #label><label for="title" font-600>标题</label></template>
      </c-input>

      <div>
        <h4 mb2 font-600>题目描述</h4>
        <markdown-editor
          v-model="problem.problem_info.problem_content.description"
        ></markdown-editor>
      </div>

      <div>
        <h4 mb2 font-600>输入格式</h4>
        <markdown-editor
          v-model="problem.problem_info.problem_content.input"
        ></markdown-editor>
      </div>

      <div>
        <h4 mb2 font-600>输出格式</h4>
        <markdown-editor
          v-model="problem.problem_info.problem_content.output"
        ></markdown-editor>
      </div>

      <div>
        <h4 mb2 font-600>提示</h4>
        <markdown-editor
          v-model="problem.problem_info.problem_content.hint"
        ></markdown-editor>
      </div>
    </div>
    <div mt4>
      <c-button color="success" @click="submit">保存</c-button>
    </div>
  </div>
</template>
