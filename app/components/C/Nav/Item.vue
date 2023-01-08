<script setup lang="ts">
import { useCNavContext } from './context';

const props = defineProps<{ to: string }>();

const route = useRoute();

const { prefix } = useCNavContext();
const { to } = toRefs(props);

const toPath = computed(() => prefix.value + to.value);

const isActive = computed(() => route.path === toPath.value);
</script>

<template>
  <div
    :class="['c-nav-item', isActive && 'active', 'cursor-pointer']"
    @click="navigateTo(toPath)"
  >
    <slot></slot>
  </div>
</template>
