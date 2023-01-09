<script setup lang="ts">
import type { Team } from '@/composables/types';

const props = withDefaults(
  defineProps<{
    team: Team;
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
