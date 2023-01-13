<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    id: string;
    options?: Array<string | number>;
    modelValue: string | number | undefined;
  }>(),
  {
    options: () => [],
  }
);

const emit = defineEmits(['update:modelValue']);

const { id, options } = toRefs(props);

const data = useVModel(props, 'modelValue', emit);
</script>

<template>
  <div class="select relative">
    <select
      :id="id"
      class="pl-2 pr-8 py-2 cursor-pointer block w-full outline-none rounded border border-1 border-[#dbdbdb] appearance-none"
      v-model="data"
    >
      <slot>
        <option :value="undefined"></option>
        <option v-for="row in options" :value="row" :selected="row === data">
          {{ row }}
        </option>
      </slot>
    </select>
  </div>
</template>
