<script setup lang="ts">
const code = ref('');

const submit = () => {};
</script>

<template>
  <div>
    <div>
      <span mr2 font-600>语言:</span>
      <span>C++</span>
    </div>
    <c-input type="textarea" id="code" v-model="code" font-mono>
      <template #label><span></span></template>
    </c-input>
    <div>
      <c-button color="success" w-full @click="submit">提交</c-button>
    </div>
  </div>
</template>
