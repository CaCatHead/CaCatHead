<script setup lang="ts">
import 'katex/dist/katex.min.css';

import { createMarkdown } from './render';
import { alias } from '@/composables/highlight';

const props = withDefaults(defineProps<{ content?: string }>(), {
  content: '',
});

const { content } = toRefs(props);

const render = createMarkdown({
  highlight: (code, lang) => {
    code = code.trim();
    lang = alias.get(lang) ?? lang;
    return highlight(code, lang).html;
  },
});

const result = computed(() => {
  return render(content.value);
});
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

.markdown-body .shiki {
  background-color: #f6f8fa !important;
}

html.dark .markdown-body .shiki {
  background-color: #24292f !important;
}
</style>
