<script setup lang="ts">
defineProps<{ user: { id: number; username: string; nickname: string } }>();
</script>

<template>
  <NuxtLink to="/">{{ user.nickname }}</NuxtLink>
</template>
