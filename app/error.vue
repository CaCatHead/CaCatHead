<script setup lang="ts">
import DefaultLayout from './layouts/default.vue';

const props = defineProps({
  error: Object,
});

useHead({
  title: '出错了 - CaCatHead',
});

const handleError = () => clearError({ redirect: '/' });
</script>

<template>
  <NuxtLayout>
    <div space-y-4>
      <h3 font-bold text-2xl justify-center flex items-center>
        <span i-carbon-warning text-3xl mr1></span>
        <span select-none>出错了</span>
      </h3>
      <div shadow-box rounded>
        <h4 border="b-1 base" p4 font-bold>错误信息</h4>
        <pre p4 overflow-auto>{{ JSON.stringify(error, null, 2) }}</pre>
      </div>
      <div>
        <c-button @click="handleError" w-full color="warning"
          >回到首页</c-button
        >
      </div>
    </div>
  </NuxtLayout>
</template>
