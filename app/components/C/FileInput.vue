<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    id: string;
    modelValue?: File[];
    color?: string;
    accept?: string;
    multiple?: boolean;
    variant?: 'fill' | 'outline' | 'light' | 'text';
  }>(),
  {
    modelValue: () => [],
    multiple: false,
    color: 'success',
    variant: 'fill',
  }
);

const emit = defineEmits<{
  (e: 'change', ev: Event): void;
  (e: 'update:modelValue', files: File[]): void;
}>();

const { id, color, variant, accept, multiple } = toRefs(props);

const files = useVModel(props, 'modelValue', emit);

const onFileChange = async (ev: Event) => {
  const target = ev.target as HTMLInputElement;
  if (!target.files) return;
  const uploaded: File[] = [];
  for (let i = 0; i < target.files.length; i++) {
    if (target.files[i]) {
      uploaded.push(target.files[i]);
    }
  }
  files.value.splice(0, files.value.length, ...uploaded);
  emit('change', ev);
};
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
      @change="onFileChange"
    />
  </div>
</template>
