<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    team: { name: string; owner: {}; members: [] };
    name?: string;
  }>(),
  {
    name: p => p.team.name,
  }
);
</script>

<template>
  <nuxt-link to="/" class="user-link">{{ name }}</nuxt-link>
</template>
