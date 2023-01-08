<script setup lang="ts">
const emit = defineEmits<{
  (e: 'submit', payload: { code: string; language: string }): void;
}>();

const code = ref('');
const language = ref('cpp');

const submit = async () => {
  emit('submit', { code: code.value, language: language.value });
};
</script>

<template>
  <div space-y-4>
    <slot></slot>
    <problem-select-language v-model="language"></problem-select-language>
    <c-input type="textarea" id="code" v-model="code" font-mono>
      <template #label><span font-600>代码</span></template>
    </c-input>
    <div>
      <c-button color="success" w-full @click="submit">提交</c-button>
    </div>
  </div>
</template>
