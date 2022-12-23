<script setup lang="ts">
definePageMeta({
  middleware(to) {
    if (to.fullPath === '/repository/' || to.fullPath === '/repository') {
      return navigateTo('/repository/1');
    }
  },
});
</script>

<template></template>
