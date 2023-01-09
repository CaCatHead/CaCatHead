<script setup lang="ts"></script>

<template>
  <div shadow-box rounded px4 py4 space-y-2>
    <div>
      <span font-bold text-xl mr4>Q</span>
      <slot name="q"></slot>
    </div>
    <div>
      <span font-bold text-xl mr4>A</span>
      <slot name="a"></slot>
    </div>
  </div>
</template>
