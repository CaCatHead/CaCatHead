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

const { team, name } = toRefs(props);
</script>

<template>
  <nuxt-link :to="`/user/${team.owner.id}`" class="user-link">{{
    name
  }}</nuxt-link>
</template>
