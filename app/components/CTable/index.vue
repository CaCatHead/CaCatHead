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
</script>

<template>
  <div>
    <table class="table w-full table-auto rounded">
      <thead select-none font-600>
        <tr>
          <slot name="headers"></slot>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in data">
          <td v-for="col in columns" p2 :class="col.class">
            <slot :name="col.name" v-bind="{ row }">{{ row[col.name] }}</slot>
          </td>
        </tr>
      </tbody>
      <tfooter>
        <slot name="footer"></slot>
      </tfooter>
    </table>
  </div>
</template>
