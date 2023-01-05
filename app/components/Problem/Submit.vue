<script setup lang="ts">
const emit = defineEmits<{
  (e: 'submit', payload: { code: string; language: string }): void;
}>();

const code = ref('');
const language = ref('cpp');
const handleSelect = (e: any) => {
  language.value = e.target?.value ?? 'cpp';
};

const submit = async () => {
  emit('submit', { code: code.value, language: language.value });
};
</script>

<template>
  <div space-y-4>
    <slot></slot>
    <div>
      <label for="language" font-600 mb2 inline-block>语言</label>
      <c-select id="language" @click="handleSelect">
        <option value="c" :selected="language === 'c'">C</option>
        <option value="cpp" :selected="language === 'cpp'">C++</option>
        <option value="java" :selected="language === 'java'">Java</option>
      </c-select>
    </div>
    <c-input type="textarea" id="code" v-model="code" font-mono>
      <template #label><span font-600>代码</span></template>
    </c-input>
    <div>
      <c-button color="success" w-full @click="submit">提交</c-button>
    </div>
  </div>
</template>
