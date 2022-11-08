<script setup lang="ts">
useHead({
  title: '比赛',
});
</script>

<template>
  <div>
    <c-table>
      <template #headers>
        <c-table-header name="name">比赛</c-table-header>
        <c-table-header name="start">比赛时间</c-table-header>
      </template>
    </c-table>
  </div>
</template>
