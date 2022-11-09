import { defineStore } from 'pinia';

export const usePolygonBus = defineStore('PolygonBus', () => {
  const counter = ref(0);

  const notify = () => {
    counter.value++;
  };

  const onEvent = (fn: () => void) => {
    watch(counter, fn);
  };

  return {
    counter,
    notify,
    onEvent,
  };
});
