<script setup lang="ts">
import type { Team } from '@/composables/types';

const props = withDefaults(
  defineProps<{
    team: Team;
    name?: string;
  }>(),
  {}
);

const { team, name: _name } = toRefs(props);

const name = computed(() => {
  return _name?.value ?? team.value.name;
});
</script>

<template>
  <nuxt-link :to="`/user/profile/${team.owner.username}`" class="user-link">
    <display-rating :rating="team.owner.rating">{{ name }}</display-rating>
  </nuxt-link>
</template>
