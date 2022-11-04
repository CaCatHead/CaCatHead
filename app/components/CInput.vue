<script setup lang="ts">
const props = defineProps<{
  id?: string;
  placeholder?: string;
  modelValue: string;
  type: string;
  color?: string;
}>();
const emit = defineEmits(['update:modelValue']);

const data = useVModel(props, 'modelValue', emit);

const color = props.color ?? 'primary';
</script>

<template>
  <div :class="['c-input-root', color]">
    <div>
      <slot name="label"></slot>
    </div>
    <div :class="['c-input-container', 'py2']">
      <input
        :id="props.id"
        :class="['c-input', 'w-full']"
        :type="props.type"
        :placeholder="props.placeholder"
        v-model="data"
      />
    </div>
  </div>
</template>

<style>
/* .c-input-container {

} */

.c-input:focus {
  border-color: var(--c-border-color);
}

.c-input {
  --c-border-color: hsl(var(--c-color));

  --at-apply: border-1 border-base rounded py2 px4;
  --at-apply: outline-none;
}
</style>
