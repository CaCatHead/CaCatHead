<script setup lang="ts">
const props = withDefaults(defineProps<{ show: boolean }>(), { show: false });

const { show } = toRefs(props);
</script>

<template>
  <div
    fixed
    top-0
    left-0
    z1000
    w-screen
    h-screen
    flex
    items-center
    justify-center
    transition-all
    :class="[show && 'bg-dark-100 bg-op-10']"
    :style="{ pointerEvents: show ? undefined : 'none' }"
  >
    <div
      v-if="show"
      transition-all
      shadow-box
      rounded
      p4
      bg-white
      dark:bg-dark
      max-h="90vh"
      max-w="90vw"
      overflow-auto
      @click.stop.prevent="show = false"
    >
      <slot></slot>
    </div>
  </div>
</template>
