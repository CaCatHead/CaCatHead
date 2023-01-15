<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: File[];
    color?: string;
    accept?: string;
    variant?: 'fill' | 'outline' | 'light' | 'text';
  }>(),
  {
    color: 'success',
    variant: 'fill',
  }
);

const emit = defineEmits<{
  (e: 'change', ev: Event): void;
  (e: 'update:modelValue', files: File[]): void;
}>();

const { color, variant, accept } = toRefs(props);

const files = useVModel(props, 'modelValue', emit);

const genId = () => 'multiple-file-input-' + randomString();
const currentId = ref(genId());
const inputs = ref<string[]>([currentId.value]);

const onFileChange = async (ev: Event, id: string) => {
  const target = ev.target as HTMLInputElement;
  if (!target.files) return;
  const selected = [...files.value];
  for (let i = 0; i < target.files.length; i++) {
    if (target.files[i]) {
      selected.push(target.files[i]);
    }
  }
  files.value = selected;
  emit('change', ev);
  // generate new fileinput
  const newId = genId();
  inputs.value.push(newId);
  currentId.value = newId;
};
</script>

<template>
  <div inline-flex items-center>
    <c-button
      tag="label"
      :for="currentId"
      :color="color"
      :variant="variant"
      flex
      items-center
      ><slot></slot
    ></c-button>
    <input
      type="file"
      v-for="id in inputs"
      :id="id"
      :name="id"
      :accept="accept"
      multiple
      hidden
      @change="ev => onFileChange(ev, id)"
    />
    <!-- <input
      type="file"
      :id="id"
      :name="id"
      :accept="accept"
      multiple
      hidden
      @change="onFileChange"
    /> -->
  </div>
</template>
