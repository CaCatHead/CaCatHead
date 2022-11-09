<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    id: string;
    color?: string;
    accept?: string;
    multiple?: boolean;
  }>(),
  {
    multiple: false,
  }
);

const emit = defineEmits<{
  (e: 'change', ev: Event): void;
}>();

const { id, color, accept, multiple } = toRefs(props);
</script>

<template>
  <div inline-block>
    <c-button
      tag="label"
      :for="id"
      :color="color"
      leading-none
      flex
      items-center
      ><slot></slot
    ></c-button>
    <input
      type="file"
      :id="id"
      :name="id"
      :accept="accept"
      :multiple="multiple"
      hidden
      @change="ev => emit('change', ev)"
    />
  </div>
</template>
