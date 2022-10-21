<script setup lang="ts">
const data = ref();
$fetch('/api/hello').then(r => (data.value = r));
</script>

<template>
  <div style="text-align: center">{{ JSON.stringify(data) }}</div>
</template>
