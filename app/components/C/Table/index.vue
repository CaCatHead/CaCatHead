<script setup lang="ts" generic="T extends Record<string, any>">
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

// used for generate style class
const alignClasses = ['text-left', 'text-right', 'text-center'];
</script>

<template>
  <div w-full>
    <!-- <div v-if="breakpoints.smallerOrEqual('md') && mobile">
      <div v-for="(row, index) in data">
        <div v-for="col in columns">
          <div>{{ col.name }}</div>
          <div>
            <slot :name="col.name" v-bind="{ row, index }">{{
              row[col.name]
            }}</slot>
          </div>
        </div>
      </div>
    </div> -->
    <table class="table w-full table-auto rounded">
      <thead select-none font-600>
        <tr>
          <slot name="headers"></slot>
        </tr>
      </thead>
      <tbody divide-y dark:divide="gray/40">
        <tr v-for="(row, index) in data">
          <td
            v-for="col in columns"
            :class="['p2', 'text-' + col.align, col.class]"
          >
            <slot :name="col.name" v-bind="{ row, index }">{{
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
