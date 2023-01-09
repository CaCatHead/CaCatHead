<script setup lang="ts">
import type { User } from '@/composables/types';

defineProps<{ user: User }>();
</script>

<template>
  <nuxt-link to="/" class="user-link">{{ user.nickname }}</nuxt-link>
</template>

<style>
.user-link:hover {
  --at-apply: text-sky-700;
}
</style>
