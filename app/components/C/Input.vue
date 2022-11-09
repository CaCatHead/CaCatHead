<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    id: string;
    name?: string;
    placeholder?: string;
    modelValue: string;
    type: string;
    color?: string;
  }>(),
  {
    name: p => p.id,
    placeholder: '',
    color: 'primary',
  }
);

const emit = defineEmits(['update:modelValue']);

const data = useVModel(props, 'modelValue', emit);

const { id, name, placeholder, type, color } = toRefs(props);
</script>

<template>
  <div :class="['c-input-root', color]">
    <div>
      <slot name="label"
        ><label :for="id">{{ name }}</label></slot
      >
    </div>
    <div :class="['c-input-container', 'py2']">
      <input
        :id="id"
        :class="['c-input', 'w-full']"
        :type="type"
        :placeholder="placeholder"
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
