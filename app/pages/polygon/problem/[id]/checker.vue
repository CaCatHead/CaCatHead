<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const code = ref('');

watch(
  () => problem.value.problem_info.problem_judge.checker,
  checker => {
    if (checker === 'custom') {
      code.value = '';
      return;
    }
    for (const c of DefaultCheckers) {
      if (checker === c.name) {
        code.value = c.code;
        return;
      }
    }
  },
  { immediate: true }
);

watch(code, code => {
  for (const c of DefaultCheckers) {
    if (code === c.code) {
      if (problem.value.problem_info.problem_judge.checker !== c.name) {
        problem.value.problem_info.problem_judge.checker = c.name;
      }
      return;
    }
  }
  problem.value.problem_info.problem_judge.checker = 'custom';
});

const save = async () => {};
</script>

<template>
  <div w-full space-y-4>
    <div w-full flex gap2>
      <div flex-auto>
        <c-select
          id="checker"
          v-model="problem.problem_info.problem_judge.checker"
        >
          <option
            value="custom"
            :selected="problem.problem_info.problem_judge.checker === 'custom'"
          >
            自定义 Checker
          </option>
          <option
            v-for="checker in DefaultCheckers"
            :key="checker.name"
            :value="checker.name"
            :selected="
              problem.problem_info.problem_judge.checker === checker.name
            "
          >
            {{ checker.name }} - {{ checker.comment }}
          </option>
        </c-select>
      </div>
      <c-button color="success" @click="save">保存</c-button>
    </div>

    <client-only>
      <code-editor w-full h="500px" v-model="code"></code-editor>
      <template #fallback>
        <div w-full shadow-box p4 rounded>
          <pre w-full overflow-auto>{{ code }}</pre>
        </div>
      </template>
    </client-only>
  </div>
</template>
