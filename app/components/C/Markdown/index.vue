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
  <div class="markdown-body" v-html="result"></div>
</template>

<style>
.markdown-body > *:last-child {
  margin-bottom: 0;
}

.markdown-body {
  color: inherit;
  background-color: inherit;
}

.markdown-body ul {
  list-style-type: circle;
}

.markdown-body ol {
  list-style-type: decimal;
}
</style>
