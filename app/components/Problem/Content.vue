<script setup lang="ts">
import * as clipboard from 'clipboard-polyfill';

import type { ProblemContent } from '@/composables/types';

const notify = useNotification();

const props = defineProps<{
  content: ProblemContent;
  time: number;
  memory: number;
}>();

const { content } = toRefs(props);

async function copyToClipboard(text: string) {
  try {
    await clipboard.writeText(text);
  } catch {
    notify.danger(`样例复制失败`);
  }
}
</script>

<template>
  <div space-y-2 mb8>
    <div>
      <span font-600 mr2>时间限制</span>
      <span>{{ time }} ms</span>
    </div>
    <div>
      <span font-600 mr2>空间限制</span>
      <display-memory :memory="memory"></display-memory>
    </div>
  </div>
  <div
    class="!max-w-full !w-full text-base prose prose-truegray dark:prose-invert"
  >
    <c-markdown :content="content.description"></c-markdown>

    <h4 v-if="content.input">输入格式</h4>
    <c-markdown :content="content.input"></c-markdown>

    <h4 v-if="content.output">输出格式</h4>
    <c-markdown :content="content.output"></c-markdown>

    <h4 v-if="content.sample && content.sample.length > 0">样例</h4>
    <div v-if="content.sample && content.sample.length > 0" w-full>
      <div
        v-for="(sample, index) in content.sample"
        :key="index"
        class="mb4 w-full"
      >
        <div
          py1
          px2
          flex
          items-center
          justify-between
          select-none
          class="subtitle is-6 mb-0 border"
        >
          <span font-bold>输入</span>
          <c-button
            variant="text"
            color="info"
            text-sm
            @click="copyToClipboard(sample.input)"
            >复制</c-button
          >
        </div>
        <div>
          <pre
            border="l-1 r-1"
            my0
            p2
            bg="[#efefef]"
            dark:bg="[#101010]"
            rounded-0
            >{{ sample.input }}</pre
          >
        </div>
        <div
          py1
          px2
          flex
          items-center
          justify-between
          select-none
          class="subtitle is-6 mb-0 border"
        >
          <span font-bold>输出</span>
          <c-button
            variant="text"
            color="info"
            text-sm
            @click="copyToClipboard(sample.answer)"
            >复制</c-button
          >
        </div>
        <div>
          <pre
            border="l-1 r-1 b-1"
            my0
            p2
            bg="[#efefef]"
            dark:bg="[#101010]"
            rounded-0
            >{{ sample.answer }}</pre
          >
        </div>
      </div>
    </div>

    <h4 v-if="content.hint">提示</h4>
    <c-markdown v-if="content.hint" :content="content.hint"></c-markdown>
  </div>
</template>

<style>
.prose :where(:not(pre) > code):not(:where(.not-prose, .not-prose *))::before,
.prose :where(:not(pre) > code):not(:where(.not-prose, .not-prose *))::after {
  content: '' !important;
}
</style>
