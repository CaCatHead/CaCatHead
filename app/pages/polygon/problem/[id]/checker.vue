<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const route = useRoute();

const notify = useNotification();

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const CUSTOM = 'custom';

const code = ref(
  problem.value.problem_info.problem_judge.checker === CUSTOM
    ? problem.value.problem_info.problem_judge.custom_checker?.code ?? ''
    : ''
);

const handleSelect = () => {
  if (problem.value.problem_info.problem_judge.checker === CUSTOM) {
    code.value =
      problem.value.problem_info.problem_judge.custom_checker?.code ?? '';
  }
};

watch(
  () => problem.value.problem_info.problem_judge.checker,
  checker => {
    if (checker === CUSTOM) {
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
  problem.value.problem_info.problem_judge.checker = CUSTOM;
});

const save = async () => {
  try {
    await fetchAPI(`/api/polygon/${route.params.id}/checker`, {
      method: 'POST',
      body: {
        type: problem.value.problem_info.problem_judge.checker,
        ...(problem.value.problem_info.problem_judge.checker === 'custom'
          ? {
              code: code.value,
              language: 'cpp',
            }
          : {}),
      },
    });
    if (problem.value.problem_info.problem_judge.checker === 'custom') {
      if (problem.value.problem_info.problem_judge.custom_checker) {
        problem.value.problem_info.problem_judge.custom_checker.code =
          code.value;
      } else {
        problem.value.problem_info.problem_judge.custom_checker = {
          code: code.value,
        };
      }
    }
    notify.success('Checker 设置成功');
  } catch (error: any) {
    notify.danger('Checker 设置失败');
  }
};
</script>

<template>
  <div w-full space-y-4>
    <div w-full flex gap4>
      <div flex-auto>
        <c-select
          id="checker"
          v-model="problem.problem_info.problem_judge.checker"
          @click="handleSelect"
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
      <div text-right text-sm text-base-400>
        <span
          >你只能使用 C++ 语言，使用
          <a href="https://oi-wiki.org/tools/testlib/checker/">testlib</a> 编写
          Checker</span
        >
      </div>
      <template #fallback>
        <div w-full shadow-box p4 rounded>
          <pre w-full overflow-auto>{{ code }}</pre>
        </div>
      </template>
    </client-only>
  </div>
</template>
