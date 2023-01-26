<script>
export default {
  name: 'CTable',
};
</script>

<script setup lang="ts" generic="T extends any">
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core';

import { CTABLE, CTableColumn } from './context';

const props = withDefaults(
  defineProps<{
    data?: T[];
    rowKey?: (row: any, index: number) => string;
    rowClass?: (
      row: any,
      index: number
    ) => undefined | string | Array<undefined | string>;
    mobile?: boolean;
    border?: boolean;
  }>(),
  {
    data: () => [],
    rowKey: (_row, index) => '' + index,
    rowClass: (_row, _index) => '',
    mobile: true,
    border: false,
  }
);

const { data, mobile, border } = toRefs(props);

const columns = ref<CTableColumn[]>([]);

const getValue = (row: T, name: string) => {
  // @ts-ignore
  return row[name];
};

const enabledColumns = computed(() => columns.value.filter(c => !c.disabled));

provide(CTABLE, {
  columns,
  mobile,
  border,
});

const breakpoints = process.server
  ? undefined
  : useBreakpoints(breakpointsTailwind);
const device = process.server ? useDevice() : undefined;
const smallScreen = computed(() => {
  if (breakpoints === undefined) {
    return device?.isMobile ?? false;
  } else {
    return breakpoints.smallerOrEqual('sm').value;
  }
});

const MobileHeader = defineComponent({
  props: ['column'],
  setup(props: { column: CTableColumn }) {
    return () =>
      props.column.slots.default
        ? props.column.slots.default()
        : props.column.label;
  },
});

// used for generate style class
const alignClasses = ['text-left', 'text-right', 'text-center'];
</script>

<template>
  <div
    w-full
    :class="[
      border && 'border-1 border-base rounded-2',
      smallScreen && mobile && data.length > 0 && 'border-0',
    ]"
  >
    <div v-if="smallScreen && mobile" space-y-4>
      <div hidden>
        <slot name="headers" v-bind="{ smallScreen }"></slot>
      </div>
      <div
        v-for="(row, index) in data"
        shadow-box
        rounded
        divide-y
        dark:divide="gray/40"
      >
        <div
          v-for="col in enabledColumns"
          flex
          gap1
          items-center
          justify-between
          px4
          py2
        >
          <div font-bold>
            <mobile-header :column="col"></mobile-header>
          </div>
          <div text-right flex-1>
            <slot :name="col.name" v-bind="{ row, index, smallScreen }">{{
              getValue(row, col.name)
            }}</slot>
          </div>
        </div>
      </div>
    </div>
    <table
      v-else
      :class="['c-table', 'table', 'w-full', 'table-auto', 'border-collapse']"
    >
      <thead select-none font-600>
        <tr :class="border && 'divide-x-1'">
          <slot name="headers" v-bind="{ smallScreen }"></slot>
        </tr>
      </thead>
      <tbody divide-y dark:divide="gray/40">
        <tr
          v-for="(row, index) in data"
          :key="rowKey(row, index)"
          :class="rowClass(row, index)"
        >
          <td
            v-for="(col, idx) in enabledColumns"
            :class="[
              idx > 0 && border && 'border-l-1 border-base',
              'p2',
              'text-' + col.align,
              col.class,
            ]"
          >
            <slot :name="col.name" v-bind="{ row, index, smallScreen }">{{
              getValue(row, col.name)
            }}</slot>
          </td>
        </tr>
      </tbody>
      <tfoot>
        <slot name="footer"></slot>
      </tfoot>
    </table>

    <div v-if="data.length === 0">
      <slot name="empty"></slot>
    </div>
  </div>
</template>

<style>
.c-table th:first-of-type {
  border-top-left-radius: 0.5rem;
}
.c-table th:last-of-type {
  border-top-right-radius: 0.5rem;
}
.c-table tr:last-of-type td:first-of-type {
  border-bottom-left-radius: 0.5rem;
}
.c-table tr:last-of-type td:last-of-type {
  border-bottom-right-radius: 0.5rem;
}
</style>
