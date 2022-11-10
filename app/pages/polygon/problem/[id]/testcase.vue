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
  score: string;
}

const testcases = computed(() => {
  const map = new Map<string, Testcase>();
  for (const file of files.value) {
    if (file.name.endsWith('.in')) {
      const name = file.name.slice(0, file.name.length - 3);
      if (!map.has(name)) map.set(name, { score: '0' });
      map.get(name)!.input = file;
    } else if (file.name.endsWith('.ans')) {
      const name = file.name.slice(0, file.name.length - 4);
      if (!map.has(name)) map.set(name, { score: '0' });
      map.get(name)!.answer = file;
    }
  }
  return [...map.values()];
});
</script>

<template>
  <div>
    <div>
      <c-file-input
        id="testcase"
        @change="onUploadTestcase"
        multiple
        accept=".in, .ans"
        >上传测试用例</c-file-input
      >
    </div>
    <div mt4 shadow-box rounded divide-y>
      <div v-for="(testcase, idx) in testcases" :key="idx" w-full p4>
        <div mb2>
          <span font-bold text-lg>测试数据点 #{{ idx }}</span>
        </div>
        <div flex items-center gap4>
          <div>
            <span>输入文件</span>
            <span>{{ testcase.input?.name }}</span>
          </div>
          <div>
            <span>答案文件</span>
            <span>{{ testcase.answer?.name }}</span>
          </div>
          <div flex-auto></div>
          <div>
            <c-input
              :id="'score_' + idx"
              type="number"
              v-model="testcase.score"
            ></c-input>
          </div>
        </div>
      </div>
      <div v-if="testcases.length === 0" flex items-center justify-center h-24>
        <span>请上传测试数据</span>
      </div>
    </div>
  </div>
</template>
