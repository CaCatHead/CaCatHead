<script setup lang="ts">
useHead({
  title: '帮助',
});
</script>

<template>
  <div !max-w-full !w-full prose prose-truegray dark:prose-invert>
    <h2 text-center>常见问题及解答</h2>
    <div space-y-4>
      <q-a>
        <template #q>这是什么网站？</template>
        <template #a
          >这是<a href="https://github.com/XLoJ/CaCatHead">猫猫头</a
          >，是一个开源的在线评测系统。</template
        >
      </q-a>
      <q-a>
        <template #q>CaCatHead Online Judge 支持哪些语言？</template>
        <template #a>目前为止，你可以使用 C, C++, Java。</template>
      </q-a>
    </div>
  </div>
</template>
