<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    id: string;
    color?: string;
    accept?: string;
    multiple?: boolean;
    variant?: 'fill' | 'outline' | 'light' | 'text';
  }>(),
  {
    multiple: false,
    color: 'success',
    variant: 'fill',
  }
);

const emit = defineEmits<{
  (e: 'change', ev: Event): void;
}>();

const { id, color, variant, accept, multiple } = toRefs(props);
</script>

<template>
  <div inline-flex items-center>
    <c-button
      tag="label"
      :for="id"
      :color="color"
      :variant="variant"
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
