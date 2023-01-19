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
  <c-notification-provider>
    <NuxtLayout>
      <NuxtLoadingIndicator />
      <NuxtPage />
    </NuxtLayout>
  </c-notification-provider>
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
  background-color: white;
}

.text-link:hover, [text-link=""]:hover {
  --at-apply: text-sky-700 dark:text-sky-200;
}

html.dark {
  --at-apply: text-light-500;
  background: #222;
  color-scheme: dark;
}

/* shadow-box in dark mode */
.dark .shadow-box,
.dark [shadow-box=''] {
  box-shadow: none;
  --at-apply: border border-1 border-gray/40;
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

.text-success, [text-success=""] {
  color: hsla(var(--c-success), var(--un-text-opacity));
}
.text-info, [text-info=""] {
  color: hsla(var(--c-info), var(--un-text-opacity));
}
.text-warning, [text-warning=""] {
  color: hsla(var(--c-warning), var(--un-text-opacity));
}
.text-danger, [text-danger=""] {
  color: hsla(var(--c-danger), var(--un-text-opacity));
}

.bg-success, [bg-success=""] {
  background-color: hsla(var(--c-success), var(--un-bg-opacity));
}
.bg-info, [bg-info=""] {
  background-color: hsla(var(--c-info), var(--un-bg-opacity));
}
.bg-warning, [bg-warning=""] {
  background-color: hsla(var(--c-warning), var(--un-bg-opacity));
}
.bg-danger, [bg-danger=""] {
  background-color: hsla(var(--c-danger), var(--un-bg-opacity));
}
</style>
