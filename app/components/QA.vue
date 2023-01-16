<script setup lang="ts"></script>

<template>
  <div shadow-box rounded px4 py4 space-y-2 w-full>
    <div flex items-start w-full>
      <span font-bold text-xl inline-block w="24px">Q</span>
      <div w="[calc(100%-24px)]">
        <slot name="q"></slot>
      </div>
    </div>
    <div flex items-start w-full>
      <span font-bold text-xl inline-block w="24px">A</span>
      <div w="[calc(100%-24px)]">
        <slot name="a"></slot>
      </div>
    </div>
  </div>
</template>
