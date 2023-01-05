<script setup lang="ts">
defineProps<{ team: { name: string; owner: {}; members: [] } }>();
</script>

<template>
  <nuxt-link to="/" class="user-link">{{ team.name }}</nuxt-link>
</template>
