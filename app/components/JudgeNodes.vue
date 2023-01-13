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
  <c-table :data="nodes">
    <template #headers>
      <c-table-header name="active">状态</c-table-header>
      <c-table-header name="name">评测机</c-table-header>
      <c-table-header name="compiler">编译器版本</c-table-header>
      <c-table-header name="system">操作系统</c-table-header>
    </template>

    <template #active="{ row, smallScreen }">
      <div
        flex
        items-center
        select-none
        relative
        :class="[
          smallScreen ? 'justify-end' : 'justify-center',
          'md:[&:hover>div]:flex',
        ]"
      >
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
        <div
          absolute
          hidden
          left-0
          top="100%"
          rounded
          border="1 base"
          p2
          bg-white
          dark:bg-dark
          w-44
          justify-between
        >
          <span font-bold>通讯时延</span>
          <span ml1
            >{{
              new Date(row.information.timestamp.response).getTime() -
              new Date(row.information.timestamp.request).getTime()
            }}
            毫秒</span
          >
        </div>
      </div>
    </template>

    <template #compiler="{ row }">
      <div space-x-2 lt-md:space-y-2 m2 text-sm>
        <span
          v-if="row?.information?.compiler?.gcc"
          class="inline-block p2 bg-gray-100 dark:bg-gray-800 rounded select-none"
          >gcc {{ parseGCC(row.information.compiler.gcc) }}</span
        >
        <span
          v-if="row?.information?.compiler?.['g++']"
          class="inline-block p2 bg-gray-100 dark:bg-gray-800 rounded select-none"
          >g++ {{ parseGCC(row.information.compiler['g++']) }}</span
        >
        <span
          v-if="row?.information?.compiler?.java"
          class="inline-block p2 bg-gray-100 dark:bg-gray-800 rounded select-none"
          >Java {{ parseJava(row.information.compiler.java) }}</span
        >
      </div>
    </template>

    <template #system="{ row }">
      <span v-if="row?.information?.platform"
        >{{ row.information.platform.system }}
        {{ row.information.platform.release }}</span
      >
    </template>
  </c-table>
</template>
