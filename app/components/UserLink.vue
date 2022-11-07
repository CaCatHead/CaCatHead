<script setup lang="ts">
defineProps<{ user: { id: number; username: string; nickname: string } }>();
</script>

<template>
  <nuxt-link to="/" class="user-link">{{ user.nickname }}</nuxt-link>
</template>

<style>
.user-link:hover {
  --at-apply: text-sky-700;
}
</style>
