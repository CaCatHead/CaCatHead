<script setup lang="ts">
import type { BaseFullSubmission } from '@/composables/types';

const props = defineProps<{ submission: BaseFullSubmission }>();

const { submission } = toRefs(props);
</script>

<template>
  <div space-y-4 mt4>
    <pre font-mono p4 shadow-box rounded overflow-auto>{{
      submission.code
    }}</pre>
    <div
      v-if="submission.verdict === Verdict.CompileError"
      shadow-box
      rounded
      overflow-auto
    >
      <h3 p4 border="b-1 base" font-bold>编译信息</h3>
      <pre v-if="!!submission.detail.compile.stdout" font-mono p4>{{
        submission.detail.compile.stdout
      }}</pre>
      <pre v-else>未知编译错误</pre>
    </div>
    <div v-else-if="submission.detail.results" shadow-box rounded divide-y>
      <div
        v-for="(testcase, index) in submission.detail.results"
        px4
        py4
        sm:flex
        justify-between
        font-mono
      >
        <div
          w="2/5"
          lt-sm="w-full justify-between mb1"
          flex
          items-center
          justify-center
        >
          <h4 w="1/2" font-600>
            {{ testcase.sample ? '样例' : '测试点' }} #{{ index + 1 }}
          </h4>
          <verdict
            :verdict="testcase.verdict"
            w="1/2"
            lt-sm="text-right"
          ></verdict>
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
    </div>
    <div v-if="submission.detail.results" text-sm text-right>
      <div text-base-800 text-op-60>
        评测机 {{ submission.detail.node ?? '' }} 运行于
        {{ formatDateTime(submission.judged) }}
      </div>
    </div>
  </div>
</template>
