<script setup lang="ts">
const { data } = await useFetch('/api/ping');
</script>

<template>
  <div text-center>{{ data }}</div>
</template>
