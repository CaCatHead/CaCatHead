<script setup lang="ts">
import { useCTableContext } from './context';

const props = withDefaults(
  defineProps<{
    name: string;
    label?: string;
    width?: number | string;
    align?: 'left' | 'right' | 'center';
    rowClass?: string | string[];
  }>(),
  {
    label: p => p.name,
    align: 'center',
    rowClass: () => [],
    hiddenOnMobile: false,
  }
);

const ctx = useCTableContext();

if (ctx.columns.value.findIndex(c => c.name === props.name) === -1) {
  ctx.columns.value.push({
    name: props.name,
    label: props.label,
    class: props.rowClass,
    align: props.align,
    slots: useSlots(),
  });
}
</script>

<template>
  <th p2 border="b-2 solid #dbdbdb dark:gray/40" :width="props.width">
    <slot>{{ props.label }}</slot>
  </th>
</template>
