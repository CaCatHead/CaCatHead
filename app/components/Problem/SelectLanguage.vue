<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: string;
    inline?: boolean;
  }>(),
  {
    modelValue: 'cpp',
    inline: false,
  }
);

const emit = defineEmits(['update:modelValue']);

const language = useVModel(props, 'modelValue', emit);

const handleSelect = (e: any) => {
  language.value = e.target?.value ?? 'cpp';
};
</script>

<template>
  <div :class="[inline ? 'inline-select-language' : 'select-language']">
    <label for="language" font-600 inline-block
      ><span>语言</span
      ><span ml2 v-if="!inline"
        >(查看<nuxt-link to="/nodes" text-link>编译器版本</nuxt-link>)</span
      ></label
    >
    <c-select id="language" @click="handleSelect" v-model="language">
      <option value="c" :selected="language === 'c'">C</option>
      <option value="cpp" :selected="language === 'cpp'">C++</option>
      <option value="java" :selected="language === 'java'">Java</option>
    </c-select>
  </div>
</template>

<style>
.inline-select-language {
  --at-apply: flex gap4 items-center;
}
.select-language > label {
  --at-apply: mb2;
}
</style>
