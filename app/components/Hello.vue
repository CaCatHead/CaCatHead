<script setup lang="ts">
const { data } = await useFetchAPI('/api/ping');
</script>

<template>
  <div text-center>{{ data }}</div>
</template>
