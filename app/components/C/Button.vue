<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    variant?: 'fill' | 'outline' | 'light' | 'text';
    color?: string;
    tag?: string;
    disabled?: boolean;
    icon?: string | undefined;
  }>(),
  {
    variant: 'fill',
    color: 'primary',
    tag: 'button',
    disabled: false,
    icon: undefined,
  }
);

const { color, variant: _variant, tag, disabled, icon } = toRefs(props);

const variant = computed(() => 'c-' + _variant.value);
</script>

<template>
  <component
    :is="tag"
    :class="[
      'c-button',
      'whitespace-nowrap',
      disabled ? 'disabled' : undefined,
      icon ? 'has-icon' : undefined,
      variant,
      color,
    ]"
  >
    <slot name="icon"><span :class="[icon, 'text-xl']"></span></slot>
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

  --at-apply: inline-flex items-center justify-center rounded-2 cursor-pointer
    select-none;

  --c-bg: hsla(var(--c-color), var(--un-bg-opacity));
  background-color: var(--c-bg);
}
.c-button.has-icon {
  padding-left: 0.5em;
  padding-right: 0.5em;
}
.c-button.disabled {
  --at-apply: cursor-not-allowed;
}

.c-button.c-fill {
  --at-apply: text-white bg-op-80;
}
.c-button.c-fill.disabled {
  --at-apply: border-gray-400 text-gray-400 bg-op-0 border-1;
}
.c-button.c-fill:not(.disabled):hover {
  --at-apply: bg-op-100;
}

.c-button.c-text {
  color: hsl(var(--c-color));
  --at-apply: bg-op-0;
}
.c-button.c-text:not(.disabled):hover {
  --at-apply: bg-op-10;
}

.c-button.c-outline {
  border-color: hsl(var(--c-color));
  color: hsl(var(--c-color));
  --at-apply: bg-op-0 border-1;
}
.c-button.c-outline.disabled {
  /* border-color: hsl(var(--c-color)); */
  /* color: hsl(var(--c-color)); */
  --at-apply: border-gray-400 text-gray-400 bg-op-0 border-1;
}
.c-button.c-outline:not(.disabled):hover {
  --at-apply: bg-op-20;
}
</style>
