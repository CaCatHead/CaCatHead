<script setup lang="ts">
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
  --c-primary: 265, 97.7%, 66.3%;
  --c-success: 94.5, 100%, 39.6%;
  --c-info: 200.1, 100%, 54.3%;
  --c-warning: 42.4, 100%, 50%;
  --c-danger: 358.3, 100%, 64.9%;
}

html {
  --at-apply: text-dark-500 font-sans;
  font-weight: 400;
}

.text-link:hover {
  --at-apply: text-sky-700 dark:text-sky-200;
}

html.dark {
  --at-apply: text-light-500;
  background: #222;
  color-scheme: dark;
}

.primary {
  --c-color: var(--c-primary);
}
.success {
  --c-color: var(--c-success);
}
.info {
  --c-color: var(--c-info);
}
.warning {
  --c-color: var(--c-warning);
}
.danger {
  --c-color: var(--c-danger);
}
</style>
