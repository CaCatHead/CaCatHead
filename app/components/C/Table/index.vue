<script setup lang="ts">
import { CTABLE, CTableColumn } from './context';

const props = withDefaults(defineProps<{ data?: any[] }>(), {
  data: () => [],
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
    <table class="table w-full table-auto rounded">
      <thead select-none font-600>
        <tr>
          <slot name="headers"></slot>
        </tr>
      </thead>
      <tbody divide-y>
        <tr v-for="row in data">
          <td
            v-for="col in columns"
            p2
            :class="['text-' + col.align, col.class]"
          >
            <slot :name="col.name" v-bind="{ row }">{{ row[col.name] }}</slot>
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
