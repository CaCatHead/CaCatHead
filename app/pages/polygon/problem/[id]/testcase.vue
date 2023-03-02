<script setup lang="ts">
import type { FullPolygonProblem } from '@/composables/types';

import { zipSync, strToU8 } from 'fflate';

import { useAutoAnimate } from '@formkit/auto-animate/vue';

const props = defineProps<{ problem: FullPolygonProblem }>();

const { problem } = toRefs(props);

const notify = useNotification();

const [parent] = useAutoAnimate();

const files = ref<File[]>([]);

interface Testcase {
  name: string;
  input?: File | { name: string; size: undefined };
  answer?: File | { name: string; size: undefined };
  score: number;
  sample: boolean;
}

const trimFileEnd = (text: string) => text.replace(/\.[a-z]+$/, '');

const testcases = ref<Testcase[]>(
  problem.value.problem_info.problem_judge.testcase_detail.map(d => ({
    name: trimFileEnd(d.input),
    input: { name: d.input, size: undefined },
    answer: { name: d.answer, size: undefined },
    score: d.score,
    sample: d.sample ?? false,
  }))
);

const clear = () => {
  testcases.value.splice(0, testcases.value.length);
  files.value.splice(0, files.value.length);
};

const moveUp = (testcase: Testcase, index: number) => {
  if (index > 0) {
    testcases.value[index] = testcases.value[index - 1];
    testcases.value[index - 1] = testcase;
  }
};
const moveDown = (testcase: Testcase, index: number) => {
  if (index + 1 < testcases.value.length) {
    testcases.value[index] = testcases.value[index + 1];
    testcases.value[index + 1] = testcase;
  }
};

watch(files, files => {
  const map = new Map<string, Testcase>();
  for (const file of files) {
    const testSample = (name: string) =>
      name.indexOf('sample') !== -1 || name.indexOf('example') !== -1;
    const setInput = (name: string, file: File) => {
      if (!map.has(name)) {
        map.set(name, {
          name: trimFileEnd(file.name),
          score: 0,
          sample: testSample(file.name),
        });
      }
      map.get(name)!.input = file;
    };
    const setAnswer = (name: string, file: File) => {
      if (!map.has(name))
        map.set(name, {
          name: trimFileEnd(file.name),
          score: 0,
          sample: testSample(file.name),
        });
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

  const oldTestcases = testcases.value.filter(
    t => t.input?.size && t.answer?.size
  );
  const oldNames = new Set(oldTestcases.map(t => t.name));
  const newTestcases = [...oldTestcases];
  const curSamples: Testcase[] = [];
  const curTestcases: Testcase[] = [];
  const entries = [...map.entries()].sort((l, r) => l[0].localeCompare(r[0]));
  for (const [_key, testcase] of entries) {
    if (!oldNames.has(testcase.name)) {
      if (testcase.sample) {
        curSamples.push(testcase);
      } else {
        curTestcases.push(testcase);
      }
    }
  }
  newTestcases.push(...curSamples, ...curTestcases);

  for (const testcase of newTestcases) {
    testcase.score = Math.max(1, Math.floor(100 / newTestcases.length));
  }

  if (newTestcases.length > 0) {
    newTestcases[newTestcases.length - 1].score =
      100 - Math.floor(100 / newTestcases.length) * (newTestcases.length - 1);

    newTestcases[0].sample = true;
  }

  testcases.value = newTestcases;
});

const getAxios = useAxiosFactory();
const loading = useLoadingIndicator();

const save = async () => {
  if (files.value.length === 0) {
    notify.warning('没有上传测试用例');
    return;
  }

  const uploadFileList: Record<string, any> = {};
  const sample = [];

  const testcaseDetail = [];
  const tasks = [];

  // 读取所有测试用例
  notify.info('开始读取测试用例');

  let sampleMode = true;
  for (const testcase of testcases.value) {
    if (testcase.input && testcase.answer) {
      const inputFile = testcase.input as File;
      const answerFile = testcase.answer as File;

      tasks.push(
        (async () => {
          uploadFileList[inputFile.name] = await readFileToU8(inputFile);
        })()
      );
      tasks.push(
        (async () => {
          uploadFileList[answerFile.name] = await readFileToU8(answerFile);
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
        if (!sampleMode) {
          notify.danger('样例必须放在测试数据的前面');
          return;
        } else if (inp.length > 1024 || ans.length > 1024) {
          notify.danger('禁止上传大样例');
          return;
        } else {
          sample.push({ input: inp, answer: ans });
        }
      } else {
        sampleMode = false;
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

  try {
    loading.start();
    const axios = await getAxios();
    const formData = new FormData();
    formData.append('file', new Blob([arch]));
    await axios.post(`/api/polygon/${problem.value.display_id}/upload`, formData, {
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `form-data; filename="problem-${problem.value.display_id}.zip"`,
      },
      onUploadProgress(ev) {
        if (ev.progress !== undefined) {
          loading.update(ev.progress * 100);
        } else {
          loading.update((ev.loaded / arch.length) * 100.0);
        }
      },
    });
    notify.success(`题目 ${problem.value.title} 测试数据保存成功`);

    problem.value.problem_info.problem_content.sample = sample;
    problem.value.problem_info.problem_judge.testcase_detail = testcaseDetail;
  } catch (error: any) {
    console.error(error);
    notify.success(`题目 ${problem.value.title} 测试数据保存失败`);
  } finally {
    loading.stop();
  }
};
</script>

<template>
  <div>
    <div space-x-4>
      <c-multiple-file-input
        id="testcase"
        v-model="files"
        multiple
        accept=".a, .in, .ans, .out"
        variant="outline"
        >导入测试数据文件</c-multiple-file-input
      >
      <c-button color="danger" @click="clear">清空</c-button>
      <c-button color="success" @click="save">保存</c-button>
    </div>

    <div mt4 shadow-box rounded divide-y ref="parent">
      <div
        v-for="(testcase, idx) in testcases"
        :key="testcase.name"
        w-full
        p4
        flex
        gap4
        items-center
      >
        <div flex-1>
          <div mb2 lt-sm:mb4 flex items-center lt-sm="flex-col items-start">
            <span inline-flex items-center>
              <span font-bold text-lg>测试数据点 #{{ idx + 1 }}</span>
              <span
                v-if="!!testcase.input?.size && !!testcase.answer?.size"
                i-mdi-check
                font-bold
                ml2
                class="text-success"
              ></span>
              <span v-else i-mdi-close ml2 class="text-danger" font-bold></span>
            </span>
            <div sm:flex-auto></div>
            <span>
              <span font-bold mr2>显示为样例</span>
              <c-switch v-model="testcase.sample"></c-switch>
            </span>
          </div>
          <div flex items-center gap4 lt-sm="gap2 flex-col items-start">
            <div>
              <c-button
                color="info"
                :disabled="!testcase.input?.size"
                lt-sm:text-sm
              >
                <span mr2>输入文件</span>
                <span>{{ testcase.input?.name }}</span>
              </c-button>
            </div>
            <div>
              <c-button
                color="info"
                :disabled="!testcase.answer?.size"
                lt-sm:text-sm
              >
                <span mr2>答案文件</span>
                <span>{{ testcase.answer?.name }}</span>
              </c-button>
            </div>
            <div flex-auto lt-sm:hidden></div>
            <div>
              <c-input
                class="flex items-center"
                :id="'score_' + idx"
                type="number"
                v-model="testcase.score"
              >
                <template #label>
                  <label
                    :for="'score_' + idx"
                    inline-block
                    w10
                    mr4
                    text-lg
                    font-bold
                    >分值</label
                  >
                </template>
              </c-input>
            </div>
          </div>
        </div>
        <div flex flex-col gap2>
          <div>
            <c-button
              class="!h12"
              color="info"
              variant="outline"
              text-xl
              icon="i-carbon-caret-up"
              @click="moveUp(testcase, idx)"
            ></c-button>
          </div>
          <div flex-auto></div>
          <div>
            <c-button
              class="!h12"
              color="info"
              variant="outline"
              text-xl
              icon="i-carbon-caret-down"
              @click="moveDown(testcase, idx)"
            ></c-button>
          </div>
        </div>
      </div>
      <div
        v-if="testcases.length === 0"
        flex
        items-center
        justify-center
        h-80
        w-full
      >
        <div text-center space-y-2 mx4>
          <div font-bold>上传测试数据</div>
          <ul list-decimal space-y-1 text-left whitespace-normal pl6>
            <li>导入测试数据文件；</li>
            <li>选择测试点显示为样例，输入分数，调整顺序；</li>
            <li>重复以上步骤，设置完成后保存。</li>
          </ul>
          <div font-bold>Tips</div>
          <ul list-decimal space-y-1 text-left whitespace-normal pl6>
            <li>测试数据格式为输入文件 xxx.in 对应答案文件 xxx.ans；</li>
            <li>除此以外还支持：xxx.in / xxx.out 和 xxx / xxx.a；</li>
            <li>文件名包含 example 或 sample 会被自动识别为样例；</li>
            <li>只要不离开页面，你可以多次导入测试数据文件。</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
