<script lang="ts">
export default {
  name: 'CTableHeader',
};
</script>

<script setup lang="ts">
import { useCTableContext } from './context';

const props = withDefaults(
  defineProps<{
    name: string;
    disabled?: boolean;
    label?: string;
    width?: number | string;
    align?: 'left' | 'right' | 'center';
    rowClass?: string | string[];
  }>(),
  {
    disabled: false,
    label: p => p.name,
    align: 'center',
    rowClass: () => [],
    hiddenOnMobile: false,
  }
);

const { disabled } = toRefs(props);

const ctx = useCTableContext();

if (ctx.columns.value.findIndex(c => c.name === props.name) === -1) {
  ctx.columns.value.push({
    name: props.name,
    disabled: disabled,
    label: props.label,
    class: props.rowClass,
    align: props.align,
    slots: useSlots(),
  });
}
</script>

<template>
  <th
    v-if="!disabled"
    p2
    border="b-2 solid #dbdbdb dark:gray/40"
    :class="[ctx.border.value && 'border-base bg-gray-100 dark:bg-dark-100']"
    :width="props.width"
  >
    <slot>{{ props.label }}</slot>
  </th>
</template>
