<script setup lang="ts">
const title = ref('');
</script>

<template>
  <div>
    <div flex mb8 items-center>
      <div>
        <h2 text-2xl font-bold mb4>创建新的题目</h2>
      </div>
    </div>
    <div mb8>
      <c-input
        mt4
        id="title"
        name="标题"
        type="text"
        color="success"
        v-model="title"
      >
      </c-input>
    </div>
    <div>
      <c-button color="success">创建</c-button>
    </div>
  </div>
</template>
