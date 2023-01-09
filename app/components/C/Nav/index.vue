<script setup lang="ts">
import { CNAV } from './context';

const props = withDefaults(defineProps<{ prefix?: string }>(), { prefix: '/' });

const { prefix } = toRefs(props);

provide(CNAV, { prefix });
</script>

<template>
  <div select-none overflow-y-hidden whitespace-nowrap class="c-nav">
    <slot></slot>
  </div>
</template>
