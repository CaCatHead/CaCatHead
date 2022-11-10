<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const files = ref<File[]>([]);

const onUploadTestcase = (ev: Event) => {
  const target = ev.target as HTMLInputElement;
  if (!target.files) return;
  const uploaded: File[] = [];
  for (let i = 0; i < target.files.length; i++) {
    if (target.files[i]) {
      uploaded.push(target.files[i]);
    }
  }
  files.value.splice(0, files.value.length, ...uploaded);
};

interface Testcase {
  input?: File;
  answer?: File;
  score: number;
  sample: boolean;
}

const testcases = computed(() => {
  if (files.value.length === 0) {
    return problem.value.problem_info.problem_judge.testcase_detail.map(d => ({
      input: { name: d.in },
      answer: { name: d.ans },
      score: d.score,
      sample: d.sample ?? false,
    }));
  }

  const map = new Map<string, Testcase>();
  for (const file of files.value) {
    if (file.name.endsWith('.in')) {
      const name = file.name.slice(0, file.name.length - 3);
      if (!map.has(name)) map.set(name, { score: 0, sample: false });
      map.get(name)!.input = file;
    } else if (file.name.endsWith('.ans')) {
      const name = file.name.slice(0, file.name.length - 4);
      if (!map.has(name)) map.set(name, { score: 0, sample: false });
      map.get(name)!.answer = file;
    }
  }
  const testcases = [...map.values()];
  for (const testcase of testcases) {
    testcase.score = Math.max(1, Math.floor(100 / testcases.length));
  }
  if (testcases.length > 0) {
    testcases[testcases.length - 1].score =
      100 - Math.floor(100 / testcases.length) * (testcases.length - 1);
  }
  return testcases;
});
</script>

<template>
  <div>
    <div space-x-4>
      <c-file-input
        id="testcase"
        @change="onUploadTestcase"
        multiple
        accept=".in, .ans"
        variant="outline"
        >导入测试用例文件</c-file-input
      >
      <c-button color="success">保存</c-button>
    </div>
    <div mt4 shadow-box rounded divide-y>
      <div v-for="(testcase, idx) in testcases" :key="idx" w-full p4>
        <div mb2 flex items-center>
          <span font-bold text-lg>测试数据点 #{{ idx + 1 }}</span>
          <div flex-auto></div>
          <span font-bold mr2>显示为样例</span>
          <c-switch v-model="testcase.sample"></c-switch>
        </div>
        <div flex items-center gap4>
          <div>
            <c-button color="info">
              <span mr2>输入文件</span>
              <span>{{ testcase.input?.name }}</span>
            </c-button>
          </div>
          <div>
            <c-button color="info">
              <span mr2>答案文件</span>
              <span>{{ testcase.answer?.name }}</span>
            </c-button>
          </div>
          <div flex-auto></div>
          <div>
            <c-input
              class="flex items-center"
              :id="'score_' + idx"
              type="number"
              v-model="testcase.score"
            >
              <template #label>
                <label :for="'score_' + idx" mr4 text-lg font-bold>分值</label>
              </template>
            </c-input>
          </div>
        </div>
      </div>
      <div v-if="testcases.length === 0" flex items-center justify-center h-24>
        <span>请上传测试数据</span>
      </div>
    </div>
  </div>
</template>
