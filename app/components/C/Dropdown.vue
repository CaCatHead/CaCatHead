<script setup lang="ts"></script>

<template>
  <div relative z10 class="[&:hover>.c-dropdown]:block">
    <div><slot></slot></div>
    <div class="c-dropdown" hidden absolute top-full>
      <slot name="dropdown"></slot>
    </div>
  </div>
</template>
