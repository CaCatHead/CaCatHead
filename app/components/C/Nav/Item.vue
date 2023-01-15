<script setup lang="ts">
import { useCNavContext } from './context';

const props = defineProps<{ to: string }>();

const route = useRoute();

const { prefix } = useCNavContext();
const { to } = toRefs(props);

const toPath = computed(() => prefix.value + to.value);

const trimEnd = (p: string) => {
  if (p.endsWith('/')) return p.substring(0, p.length - 1);
  else return p;
};

const isActive = computed(() => {
  return trimEnd(route.path) === trimEnd(toPath.value);
});
</script>

<template>
  <nuxt-link
    :class="[
      'block',
      'c-nav-item',
      isActive && 'active',
      'inline-block',
      'cursor-pointer',
    ]"
    :to="toPath"
  >
    <slot></slot>
  </nuxt-link>
</template>
