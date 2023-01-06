<script setup lang="ts">
import 'katex/dist/katex.min.css';

import { createMarkdown } from './render';

const props = withDefaults(defineProps<{ content?: string }>(), {
  content: '',
});

const { content } = toRefs(props);

const render = createMarkdown();

const result = computed(() => render(content.value));
</script>

<template>
  <div class="markdown-body">
    <div v-html="result"></div>
  </div>
</template>
