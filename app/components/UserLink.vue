<script setup lang="ts">
import type { User } from '@/composables/types';

const props = defineProps<{ user: User }>();

const { user } = toRefs(props);
</script>

<template>
  <nuxt-link :to="`/user/${user.id}`" class="user-link">{{
    user.nickname
  }}</nuxt-link>
</template>

<style>
.user-link:hover {
  --at-apply: text-sky-700;
}
</style>
