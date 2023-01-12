<script setup lang="ts">
import { format } from 'date-fns';

const timestamp = useServerTimestamp();

const formatCNDateTime = (date: string | number | Date) =>
  format(new Date(date), 'M 月 d 日 H 时 m 分 s 秒');
</script>

<template>
  <div flex="~" items-center text-sm text-base-500 font-mono>
    <span>服务器时间 {{ formatCNDateTime(timestamp) }}</span>
  </div>
</template>
