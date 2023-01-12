<script setup lang="ts" generic="T extends string | number">
const props = withDefaults(
  defineProps<{
    id: string;
    name?: string;
    placeholder?: string;
    modelValue: T;
    type: string;
    color?: string;
  }>(),
  {
    name: p => p.id,
    placeholder: '',
    color: 'info',
  }
);

const attr = useAttrs();

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
    <div :class="['c-input-container', 'py2']" flex items-center>
      <input
        v-if="type !== 'textarea'"
        :id="id"
        :class="['c-input', 'w-full']"
        :type="type"
        :placeholder="placeholder"
        v-model="data"
        @change="attr.onChange"
        @click="attr.onClick"
        @focus="attr.onFocus"
        @focusin="attr.onFocusin"
        @focusout="attr.onFocusout"
        @input="attr.onInput"
        @keyup="attr.onKeyup"
        @mouseenter="attr.onMouseenter"
        @mouseleave="attr.onMouseleave"
        @mousemove="attr.onMousemove"
      />
      <textarea
        v-else
        :name="name"
        :id="id"
        :class="['c-input', 'c-input-textarea', 'w-full']"
        rows="10"
        v-model="data"
      ></textarea>
      <div flex-1>
        <slot name="end"></slot>
      </div>
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

.c-input.c-input-textarea {
  --at-apply: p2;
}
</style>
