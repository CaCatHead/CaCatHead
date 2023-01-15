<script setup lang="ts">
import { CModalSymbol } from './context';

const props = withDefaults(defineProps<{ show: boolean }>(), { show: false });

const emit = defineEmits(['open', 'close']);

const ctx = inject(CModalSymbol)!;

const { show } = toRefs(props);

ctx.show.value = show.value;
watch(show, show => {
  if (ctx.show.value !== show) {
    ctx.show.value = show;
  }
});
watch(
  () => ctx.show.value,
  ctx => {
    if (ctx !== show.value) {
      if (ctx) {
        emit('open');
      } else {
        emit('close');
      }
    }
  }
);
</script>

<template>
  <Teleport to="#c-modal-container">
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
    >
      <slot></slot>
    </div>
  </Teleport>
</template>
