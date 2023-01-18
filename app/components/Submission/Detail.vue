<script setup lang="ts">
import type { BaseFullSubmission } from '@/composables/types';

import { default as AnsiUp } from 'ansi_up';

const props = defineProps<{ submission: BaseFullSubmission }>();

const { submission } = toRefs(props);

const expand = ref([] as boolean[]);

watch(
  submission,
  () => {
    const res = submission.value.detail?.results ?? [];
    expand.value.splice(0, expand.value.length, ...res.map(_ => false));
  },
  { immediate: true }
);

const parser = new AnsiUp();

const compileOutput = computed(() => {
  if (submission.value.detail?.compile?.stdout) {
    return parser.ansi_to_html(submission.value.detail?.compile?.stdout);
  } else if (submission.value.detail?.compile?.stderr) {
    return parser.ansi_to_html(submission.value.detail?.compile?.stderr);
  } else {
    return '';
  }
});
</script>

<template>
  <div space-y-4 mt4>
    <code-box
      :code="submission.code"
      :language="submission.language"
    ></code-box>
    <div
      v-if="
        submission.verdict === Verdict.CompileError ||
        submission.detail?.compile?.stderr ||
        submission.detail?.compile?.stdout
      "
      shadow-box
      rounded
      overflow-auto
    >
      <h3 p4 w-full font-bold>编译信息</h3>
      <pre
        v-if="compileOutput"
        font-mono
        p4
        overflow-auto
        border="t-1 base"
        lt-sm:text-xs
        v-html="compileOutput"
      ></pre>
      <pre v-else font-mono p4 border="t-1 base">未知编译错误</pre>
    </div>
    <div
      v-else-if="
        submission.detail.results && submission.detail.results.length > 0
      "
      shadow-box
      rounded
      divide-y
      dark:divide="gray/40"
    >
      <div
        v-for="(testcase, index) in submission.detail.results"
        px4
        py4
        font-mono
        transition-all
        text-base-900
        hover:text-op-100
        :class="expand[index] ? 'text-op-100' : 'text-op-60'"
      >
        <div
          sm:flex
          justify-between
          select-none
          cursor-pointer
          @click="() => (expand[index] = !expand[index])"
        >
          <div
            w="2/5"
            lt-sm="w-full justify-between mb1"
            flex
            items-center
            justify-center
          >
            <h4 w="1/2" font-600 inline-flex items-center gap1>
              <span
                text-xl
                :class="
                  expand[index] ? 'i-carbon-caret-down' : 'i-carbon-caret-right'
                "
              ></span>
              <span
                >{{ testcase.sample ? '样例' : '测试点' }} #{{
                  index + 1
                }}</span
              >
            </h4>
            <display-verdict
              :verdict="testcase.verdict"
              w="1/2"
              lt-sm="text-right"
            ></display-verdict>
          </div>
          <div
            w="3/5"
            lt-sm="w-full justify-between"
            flex
            items-center
            justify-center
          >
            <span
              w="1/3"
              inline-flex
              items-center
              v-if="testcase.score !== undefined && testcase.score !== null"
            >
              <span i-carbon-checkmark-outline text-lg mr1></span>
              <span>{{ testcase.score }} pts</span>
            </span>
            <span w="1/3" inline-flex items-center lt-sm="justify-center">
              <span i-carbon-time text-lg mr1></span>
              <span>{{ testcase.time }} ms</span>
            </span>
            <span w="1/3" inline-flex items-center lt-sm="justify-end">
              <span i-carbon-chip text-lg mr1></span>
              <span>{{ testcase.memory }} KB</span>
            </span>
          </div>
        </div>

        <div v-show="expand[index]" mt4>
          <div flex items-center lt-sm="flex-col items-start">
            <div text-sm font-bold sm:w="1/5">Checker 运行信息</div>
            <div space-x-4 sm:w="1/5" v-if="testcase.checker">
              <span inline-flex items-center lt-sm="justify-center">
                <span i-carbon-time text-lg mr1></span>
                <span>{{ testcase.checker?.time }} ms</span>
              </span>
              <span inline-flex items-center lt-sm="justify-end">
                <span i-carbon-chip text-lg mr1></span>
                <span>{{ testcase.checker?.memory }} KB</span>
              </span>
            </div>
          </div>
          <div shadow-box rounded p2 mt2 v-if="testcase.message">
            <pre whitespace-normal>{{ testcase.message }}</pre>
          </div>
        </div>
      </div>
    </div>
    <div v-if="submission.detail?.node" text-sm text-right>
      <div text-base-800 text-op-60>
        评测机 {{ submission.detail.node ?? '' }} 运行于
        {{ formatDateTime(submission.judged) }}
      </div>
    </div>
  </div>
</template>
