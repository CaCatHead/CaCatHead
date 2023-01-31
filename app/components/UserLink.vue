<script setup lang="ts">
import type { User } from '@/composables/types';

const props = defineProps<{ user: User }>();

const { user } = toRefs(props);
</script>

<template>
  <nuxt-link :to="`/user/profile/${user.username}`" class="user-link">
    <display-rating :rating="user.rating" :rank="user.rank">{{
      user.nickname
    }}</display-rating>
  </nuxt-link>
</template>

<style>
.user-link:hover {
  --at-apply: text-sky-700;
}
</style>
