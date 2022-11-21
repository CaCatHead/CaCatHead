<script setup lang="ts">
import { CNAV } from './context';

const props = withDefaults(defineProps<{ prefix?: string }>(), { prefix: '/' });

const { prefix } = toRefs(props);

provide(CNAV, { prefix });
</script>

<template>
  <div flex items-center gap2 select-none class="c-nav">
    <slot></slot>
  </div>
</template>
