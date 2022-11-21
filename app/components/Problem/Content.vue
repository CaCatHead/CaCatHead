<script setup lang="ts">
import type { ProblemContent } from '@/composables/types';

const props = defineProps<{ content: ProblemContent }>();

const { content } = toRefs(props);

async function copyToClipboard(text: string) {
  await navigator.clipboard.writeText(text);
}
</script>

<template>
  <div class="!max-w-full !w-full text-base prose prose-truegray">
    <h4>题目描述</h4>
    <c-markdown :content="content.description"></c-markdown>

    <h4>输入格式</h4>
    <c-markdown :content="content.input"></c-markdown>

    <h4>输出格式</h4>
    <c-markdown :content="content.output"></c-markdown>

    <h4>样例</h4>
    <div w-full>
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
          <pre border="l-1 r-1" my0 p2 bg="[#efefef]" rounded-0>{{
            sample.input
          }}</pre>
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
          <pre border="l-1 r-1 b-1" my0 p2 bg="[#efefef]" rounded-0>{{
            sample.answer
          }}</pre>
        </div>
      </div>
    </div>

    <h4 v-if="content.hint">提示</h4>
    <c-markdown v-if="content.hint" :content="content.hint"></c-markdown>
  </div>
</template>
