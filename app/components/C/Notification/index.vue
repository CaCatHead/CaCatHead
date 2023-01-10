<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    variant?: 'fill' | 'outline' | 'light';
    color?: string;
  }>(),
  {
    variant: 'fill',
    color: 'info',
  }
);

const { variant: _variant, color } = toRefs(props);

const variant = computed(() => 'c-' + _variant.value);
</script>

<template>
  <div inline-block rounded px4 py2 :class="['c-notification', variant, color]">
    <slot></slot>
  </div>
</template>

<style>
.c-notification {
  --c-bg: hsla(var(--c-color), var(--un-bg-opacity));
  background-color: var(--c-bg);
}

.c-notification.c-fill {
  --at-apply: text-white bg-op-100;
}
</style>
