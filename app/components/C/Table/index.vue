<script setup lang="ts" generic="T extends Record<string, any>">
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core';

import { CTABLE, CTableColumn } from './context';

const props = withDefaults(defineProps<{ data?: T[]; mobile?: boolean }>(), {
  data: () => [],
  mobile: true,
});

const { data } = toRefs(props);

const columns = ref<CTableColumn[]>([]);

provide(CTABLE, {
  columns,
});

const breakpoints = useBreakpoints(breakpointsTailwind);
const smallScreen = computed(() => breakpoints.smallerOrEqual('sm').value);

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
  <div w-full>
    <div v-if="smallScreen && mobile" space-y-4>
      <div hidden>
        <slot
          name="headers"
          :breakpoints="breakpoints"
          :small-screen="smallScreen"
        ></slot>
      </div>
      <div
        v-for="(row, index) in data"
        shadow-box
        rounded
        divide-y
        dark:divide="gray/40"
      >
        <div
          v-for="col in columns"
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
              row[col.name]
            }}</slot>
          </div>
        </div>
      </div>
    </div>
    <table v-else class="table w-full table-auto rounded">
      <thead select-none font-600>
        <tr>
          <slot
            name="headers"
            :breakpoints="breakpoints"
            :small-screen="smallScreen"
          ></slot>
        </tr>
      </thead>
      <tbody divide-y dark:divide="gray/40">
        <tr v-for="(row, index) in data">
          <td
            v-for="col in columns"
            :class="['p2', 'text-' + col.align, col.class]"
          >
            <slot :name="col.name" v-bind="{ row, index, smallScreen }">{{
              row[col.name]
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
