<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

import { zipSync, strToU8 } from 'fflate';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const notify = useNotification();

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
      input: { name: d.input, size: undefined },
      answer: { name: d.answer, size: undefined },
      score: d.score,
      sample: d.sample ?? false,
    }));
  }

  const map = new Map<string, Testcase>();
  for (const file of files.value) {
    const setInput = (name: string, file: File) => {
      if (!map.has(name)) map.set(name, { score: 0, sample: false });
      map.get(name)!.input = file;
    };
    const setAnswer = (name: string, file: File) => {
      if (!map.has(name)) map.set(name, { score: 0, sample: false });
      map.get(name)!.answer = file;
    };

    // CaCatHead 使用的测试数据后缀名格式: .in / .ans, .out
    // Codeforces 使用的测试数据后缀名格式: 无后缀 / .a
    if (file.name.endsWith('.in')) {
      const name = file.name.slice(0, file.name.length - 3);
      setInput(name, file);
    } else if (file.name.endsWith('.ans') || file.name.endsWith('.out')) {
      const name = file.name.slice(0, file.name.length - 4);
      setAnswer(name, file);
    } else if (file.name.endsWith('.a')) {
      const name = file.name.slice(0, file.name.length - 2);
      setAnswer(name, file);
    } else if (file.name.indexOf('.') === -1) {
      setInput(file.name, file);
    }
  }

  const testcases = [...map.values()];
  for (const testcase of testcases) {
    testcase.score = Math.max(1, Math.floor(100 / testcases.length));
  }

  if (testcases.length > 0) {
    testcases[testcases.length - 1].score =
      100 - Math.floor(100 / testcases.length) * (testcases.length - 1);

    testcases[0].sample = true;
  }

  return testcases;
});

const save = async () => {
  if (files.value.length === 0) {
    notify.warning('没有上传测试用例');
    return;
  }

  const readFileContent = (file: File): Promise<string> => {
    return new Promise(res => {
      const reader = new FileReader();
      reader.addEventListener('loadend', ev => {
        res((ev.target?.result as string) ?? '');
      });
      reader.readAsText(file);
    });
  };
  const fileToU8 = (file: File): Promise<Uint8Array> => {
    return new Promise(res => {
      const reader = new FileReader();
      reader.addEventListener('loadend', ev => {
        const buffer: ArrayBuffer = ev.target?.result! as ArrayBuffer;
        res(new Uint8Array(buffer));
      });
      reader.readAsArrayBuffer(file);
    });
  };

  const uploadFileList: Record<string, any> = {};
  const sample = [];

  const testcaseDetail = [];
  const tasks = [];

  // 读取所有测试用例
  notify.info('开始读取测试用例');
  for (const testcase of testcases.value) {
    if (testcase.input && testcase.answer) {
      const inputFile = testcase.input as File;
      const answerFile = testcase.answer as File;

      tasks.push(
        (async () => {
          uploadFileList[inputFile.name] = await fileToU8(inputFile);
        })()
      );
      tasks.push(
        (async () => {
          uploadFileList[answerFile.name] = await fileToU8(answerFile);
        })()
      );

      testcaseDetail.push({
        input: testcase.input.name,
        answer: testcase.answer.name,
        score: testcase.score,
        sample: testcase.sample,
      });

      // 手动读取样例
      if (testcase.sample) {
        const inp = await readFileContent(testcase.input as File);
        const ans = await readFileContent(testcase.answer as File);
        if (inp.length > 1024 || ans.length > 1024) {
          // 不应该上传这么大的样例
        }
        sample.push({ input: inp, answer: ans });
      }
    }
  }
  await Promise.all(tasks);

  const config = {
    problem: {
      sample,
    },
    testcases: testcaseDetail,
  };

  notify.info('开始打包测试用例');
  const arch = zipSync(
    {
      ...uploadFileList,
      'config.json': strToU8(JSON.stringify(config, null, 2)),
    },
    { level: 4, mtime: new Date() }
  );

  notify.info('开始上传测试用例');
  const formData = new FormData();
  formData.append('file', new Blob([arch]));
  await fetchAPI(`/api/polygon/${problem.value.id}/upload`, {
    method: 'POST',
    body: formData,
    headers: {
      'Content-Type': 'application/zip',
      'Content-Disposition': `form-data; filename="problem-${problem.value.id}.zip"`,
    },
  });

  notify.success(`题目 ${problem.value.title} 测试数据保存成功`);

  problem.value.problem_info.problem_content.sample = sample;
  problem.value.problem_info.problem_judge.testcase_detail = testcaseDetail;
};
</script>

<template>
  <div>
    <div space-x-4>
      <c-file-input
        id="testcase"
        @change="onUploadTestcase"
        multiple
        accept=".a, .in, .ans, .out"
        variant="outline"
        >导入测试用例文件</c-file-input
      >
      <c-button color="success" @click="save">保存</c-button>
    </div>

    <div mt4 shadow-box rounded divide-y>
      <div v-for="(testcase, idx) in testcases" :key="idx" w-full p4>
        <div mb2 flex items-center>
          <span font-bold text-lg>测试数据点 #{{ idx + 1 }}</span>
          <span
            v-if="!!testcase.input?.size && !!testcase.answer?.size"
            i-mdi-check
            font-bold
            ml2
            class="text-success"
          ></span>
          <span v-else i-mdi-close ml2 class="text-danger" font-bold></span>
          <div flex-auto></div>
          <span font-bold mr2>显示为样例</span>
          <c-switch v-model="testcase.sample"></c-switch>
        </div>
        <div flex items-center gap4>
          <div>
            <c-button color="info" v-if="!!testcase.input?.size">
              <span mr2>输入文件</span>
              <span>{{ testcase.input?.name }}</span>
            </c-button>
          </div>
          <div>
            <c-button color="info" v-if="!!testcase.answer?.size">
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
