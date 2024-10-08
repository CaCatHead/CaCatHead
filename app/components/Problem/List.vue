<script setup lang="ts">
import type { Problem } from '@/composables/types';

import { Verdict } from '@/composables/verdict';

const props = withDefaults(
  defineProps<{
    problems: Problem[];
    problemLink: (problem: Problem, index: number) => string;
    problemIndex?: (problem: Problem, index: number) => string;
    problemVerdict?: (problem: Problem, index: number) => Verdict | undefined;
    operationWidth?: string;
  }>(),
  {
    problemIndex: (p: Problem) => String(p.display_id),
    operationWidth: '60px',
  }
);

const { problems, problemVerdict } = toRefs(props);

const getBg = (row: Problem, index: number) => {
  if (problemVerdict?.value) {
    const verdict = problemVerdict.value(row, index);
    if (verdict) {
      return verdict === Verdict.Accepted
        ? '[&>td:first-child]:bg-[#e0ffe4] [&>td:first-child]:dark:bg-[#56ca00] [&>td:first-child]:text-neutral-900'
        : '[&>td:first-child]:bg-[#ffe3e3] [&>td:first-child]:dark:bg-[#ca0056] [&>td:first-child]:text-neutral-900';
    } else {
      return '';
    }
  } else {
    return '';
  }
};

const emit = defineEmits<{
  (e: 'submit', problem: Problem): Promise<void>;
}>();
</script>

<template>
  <c-table :data="problems" border :mobile="false" :row-class="getBg">
    <template #headers="{ smallScreen }">
      <c-table-header name="display_id" width="60">#</c-table-header>
      <c-table-header name="title" align="left" text-left>题目</c-table-header>
      <c-table-header
        :disabled="smallScreen"
        name="operation"
        :width="operationWidth"
        ><span></span
      ></c-table-header>
    </template>
    <template #display_id="{ row, index }">
      <nuxt-link :to="problemLink(row, index)" class="text-link font-bold">{{
        problemIndex(row, index)
      }}</nuxt-link>
    </template>
    <template #title="{ row, index }">
      <div flex justify-between items-center lt-md="items-start flex-col gap1">
        <nuxt-link :to="problemLink(row, index)" class="text-link">{{
          row.title
        }}</nuxt-link>
        <div
          text-xs
          text-base-800
          text-op-60
          inline-flex
          items-end
          md="flex-col w-32 gap1"
          lt-md="gap2"
        >
          <span inline-flex items-center justify-start>
            <span i-carbon-time text-lg mr1></span>
            <span>{{ row.time_limit }} ms</span>
          </span>
          <span inline-flex items-center justify-start>
            <span i-carbon-chip text-lg mr1></span>
            <display-memory :memory="row.memory_limit"></display-memory>
          </span>
        </div>
      </div>
    </template>
    <template #operation="{ row, index }">
      <slot name="operation" v-bind="{ row, index }">
        <c-button
          variant="text"
          color="success"
          icon="i-akar-icons-paper-airplane"
          @click="emit('submit', row)"
        ></c-button>
      </slot>
    </template>

    <template #empty>
      <div h="36" text-xl font-bold flex items-center justify-center>
        没有题目
      </div>
    </template>
  </c-table>
</template>
