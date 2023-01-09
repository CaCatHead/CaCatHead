<script setup lang="ts"></script>

<template>
  <div shadow-box rounded px4 py4 space-y-2 w-full>
    <div flex items-start w-full>
      <span font-bold text-xl mr4>Q</span>
      <div flex-auto>
        <slot name="q"></slot>
      </div>
    </div>
    <div flex items-start w-full>
      <span font-bold text-xl mr4>A</span>
      <div flex-auto>
        <slot name="a"></slot>
      </div>
    </div>
  </div>
</template>
