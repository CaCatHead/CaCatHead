<script setup lang="ts">
import type { JudgeNode } from '@/composables/types';

const props = defineProps<{
  nodes: JudgeNode[];
}>();

const { nodes } = toRefs(props);

const parseGCC = (text: string) => {
  const first = text.split('\n')[0];
  return /(\d+\.\d+\.\d+)/.exec(first)![1];
};

const parseJava = (text: string) => {
  return /version "(\d+\.\d+\.\d+)"/.exec(text)![1];
};
</script>

<template>
  <div>
    <c-table :data="nodes">
      <template #headers>
        <c-table-header name="active">状态</c-table-header>
        <c-table-header name="name">评测机</c-table-header>
        <c-table-header name="compiler">编译器版本</c-table-header>
        <c-table-header name="system">操作系统</c-table-header>
      </template>

      <template #active="{ row }">
        <div flex items-center justify-center>
          <span
            inline-block
            h-4
            w-4
            rounded-full
            mr2
            :class="['bg-op-100', row.active ? 'bg-success' : 'bg-danger']"
          ></span>
          <span v-if="row.active">在线</span>
          <span v-else>离线</span>
        </div>
      </template>

      <template #compiler="{ row }">
        <div space-x-2 m2>
          <span
            class="inline-block p2 bg-gray-100 dark:bg-gray-800 rounded select-none"
            >gcc {{ parseGCC(row.information.compiler.gcc) }}</span
          >
          <span
            class="inline-block p2 bg-gray-100 dark:bg-gray-800 rounded select-none"
            >g++ {{ parseGCC(row.information.compiler['g++']) }}</span
          >
          <span
            class="inline-block p2 bg-gray-100 dark:bg-gray-800 rounded select-none"
            >Java {{ parseJava(row.information.compiler.java) }}</span
          >
        </div>
      </template>

      <template #system="{ row }">
        <span
          >{{ row.information.platform.system }}
          {{ row.information.platform.release }}</span
        >
      </template>
    </c-table>
  </div>
</template>
