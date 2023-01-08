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
      source: problem.value.problem_info.problem_content.source ?? '',
      time_limit: problem.value.time_limit,
      memory_limit: problem.value.memory_limit,
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

      <c-input id="time_limit" type="number" v-model="problem.time_limit">
        <template #label
          ><label for="time_limit" font-600
            >时间限制 (单位: ms)</label
          ></template
        >
      </c-input>

      <c-input id="memory_limit" type="number" v-model="problem.memory_limit">
        <template #label
          ><label for="memory_limit" font-600
            >空间限制 (单位: KB)</label
          ></template
        >
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

      <c-input
        id="source"
        type="text"
        v-model="problem.problem_info.problem_content.source"
      >
        <template #label><label for="source" font-600>来源</label></template>
      </c-input>
    </div>
    <div mt4>
      <c-button color="success" @click="submit">保存</c-button>
    </div>
  </div>
</template>
