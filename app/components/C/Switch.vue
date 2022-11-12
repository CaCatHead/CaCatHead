<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    id?: string;
    variant?: 'fill' | 'outline' | 'light' | 'text';
    color?: string;
    modelValue: boolean;
  }>(),
  {
    id: () => 'c-radio-' + randomString(),
    variant: 'fill',
    color: 'primary',
    modelValue: false,
  }
);

const emit = defineEmits(['update:modelValue', 'change']);

const { id, modelValue } = toRefs(props);
const flag = ref(modelValue.value);

watch(modelValue, modelValue => (flag.value = modelValue));
watch(flag, flag => {
  emit('update:modelValue', flag);
  emit('change', flag);
});
</script>

<template>
  <label
    :for="id"
    inline-flex
    justify-center
    items-center
    cursor-pointer
    class="c-switch"
  >
    <input
      :id="id"
      type="checkbox"
      role="switch"
      v-model="flag"
      class="hidden"
    />
    <div
      cursor-pointer
      rounded-full
      flex
      items-center
      min-w="$c-switch-min-width"
      bg-op-100
      :class="['c-switch-container', color, flag && 'c-switch-checked']"
    >
      <div class="c-switch-dot rounded-inherit"></div>
    </div>
  </label>
</template>

<style>
:root {
  --c-switch-min-width: 3em;
  --c-switch-default-color: 220, 13%, 91%;
}

.c-switch-container {
  background-color: hsla(var(--c-switch-default-color), var(--un-bg-opacity));
}

.c-switch-container.c-switch-checked {
  justify-content: end;
  background-color: hsla(var(--c-color), var(--un-bg-opacity));
}

.c-switch-dot {
  height: 1.18em;
  width: 1.18em;
  margin: 0.25em;

  --un-bg-opacity: 1;
  background-color: rgba(255, 255, 255, var(--un-bg-opacity));

  transition-property: color, background-color, border-color,
    text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter,
    backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
  transition-duration: 200ms;
  transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
}
</style>
