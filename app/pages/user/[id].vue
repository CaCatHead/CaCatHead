<script setup lang="ts">
const route = useRoute();
</script>

<template>
  <div>
    <h3 font-bold text-xl>用户 {{ route.params.id }}</h3>
  </div>
</template>
