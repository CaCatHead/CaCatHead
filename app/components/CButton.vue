<script setup lang="ts">
const props = defineProps<{
  variant?: 'fill' | 'outline' | 'light' | 'text';
  color?: string;
}>();

const variant = 'c-' + (props.variant ?? 'fill');

const color = props.color ?? 'primary';
</script>

<template>
  <button :class="['c-button', 'whitespace-nowrap', variant, color]">
    <slot></slot>
  </button>
</template>

<style>
.c-button {
  height: 2.5em;
  border-radius: 0.5em;
  padding-left: 1em;
  padding-right: 1em;
  font-weight: 500;

  @apply rounded-2;

  --c-bg: hsla(var(--c-color), var(--un-bg-opacity));
  background-color: var(--c-bg);
}

.c-button.c-fill {
  @apply text-white bg-op-80;
}
.c-button.c-fill:hover {
  @apply bg-op-100;
}

.c-button.c-text {
  color: hsl(var(--c-color));
  @apply bg-op-0;
}
.c-button.c-text:hover {
  @apply bg-op-10;
}

.c-button.c-outline {
  border-color: hsl(var(--c-color));
  color: hsl(var(--c-color));
  @apply bg-op-0 border-1;
}
.c-button.c-outline:hover {
  @apply bg-op-20;
}
</style>
