<script setup lang="ts">
import './assets/main.css';

useHead({
  titleTemplate(title) {
    return title && title !== 'CaCatHead'
      ? `${title} - CaCatHead`
      : 'CaCatHead';
  },
});
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<style>
:root {
  --main-padding-y: 1rem;
  --main-max-width: 64rem;
}

html {
  @apply text-dark-500 font-sans;
  font-weight: 400;
}

.text-link:hover {
  @apply text-sky-700 dark:text-sky-200;
}

html.dark {
  @apply text-light-500;
  background: #222;
  color-scheme: dark;
}
</style>
