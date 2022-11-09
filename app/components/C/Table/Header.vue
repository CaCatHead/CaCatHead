<script setup lang="ts">
import { useCTableContext } from './context';

const props = withDefaults(
  defineProps<{
    name: string;
    label?: string;
    width?: number | string;
    rowClass?: string | string[];
  }>(),
  {
    label: p => p.name,
    rowClass: () => [],
  }
);
const ctx = useCTableContext();
ctx.columns.value.push({ name: props.name, class: props.rowClass });
</script>

<template>
  <th p2 border="b-2 solid #dbdbdb" :width="props.width">
    <slot>{{ props.label }}</slot>
  </th>
</template>
