<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    variant?: 'fill' | 'outline' | 'light' | 'text';
    color?: string;
    tag?: string;
  }>(),
  {
    variant: 'fill',
    color: 'primary',
    tag: 'button',
  }
);

const { color, variant: _variant, tag } = toRefs(props);

const variant = computed(() => 'c-' + _variant.value);
</script>

<template>
  <component
    :is="tag"
    :class="['c-button', 'whitespace-nowrap', variant, color]"
  >
    <slot></slot>
  </component>
</template>

<style>
.c-button {
  height: 2.5em;
  border-radius: 0.5em;
  padding-left: 1em;
  padding-right: 1em;
  font-weight: 500;

  --at-apply: inline-block rounded-2 cursor-pointer;

  --c-bg: hsla(var(--c-color), var(--un-bg-opacity));
  background-color: var(--c-bg);
}

.c-button.c-fill {
  --at-apply: text-white bg-op-80;
}
.c-button.c-fill:hover {
  --at-apply: bg-op-100;
}

.c-button.c-text {
  color: hsl(var(--c-color));
  --at-apply: bg-op-0;
}
.c-button.c-text:hover {
  --at-apply: bg-op-10;
}

.c-button.c-outline {
  border-color: hsl(var(--c-color));
  color: hsl(var(--c-color));
  --at-apply: bg-op-0 border-1;
}
.c-button.c-outline:hover {
  --at-apply: bg-op-20;
}
</style>
