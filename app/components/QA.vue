<script setup lang="ts"></script>

<template>
  <div shadow-box rounded px4 py4 space-y-2>
    <div flex items-start>
      <span font-bold text-xl mr4>Q</span>
      <div>
        <slot name="q"></slot>
      </div>
    </div>
    <div flex items-start>
      <span font-bold text-xl mr4>A</span>
      <div>
        <slot name="a"></slot>
      </div>
    </div>
  </div>
</template>
