<script setup lang="ts">
import { CModalSymbol } from './context';

const show = ref(false);

provide(CModalSymbol, { show });

const onClick = () => {
  show.value = false;
};
</script>

<template>
  <div>
    <slot></slot>
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
      @click="onClick"
    >
      <div id="c-modal-container" @click.stop.prevent></div>
    </div>
  </div>
</template>
