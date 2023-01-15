<script setup lang="ts">
import 'katex/dist/katex.min.css';

import { createMarkdown } from './render';
import {
  preSetup,
  escapeCode,
  alias,
  isLangSupport,
} from '@/composables/highlight';

const props = withDefaults(defineProps<{ content?: string }>(), {
  content: '',
});

const { content } = toRefs(props);

const isDark = useDark();

const highlighter = await preSetup();

const render = createMarkdown({
  highlight: (code, lang) => {
    code = code.trim();
    lang = alias.get(lang) ?? lang;
    if (highlighter && isLangSupport(lang)) {
      return highlighter.codeToHtml(code, {
        lang,
        theme: isDark.value ? 'Eva Dark' : 'Eva Light',
      });
    } else {
      return escapeCode(code);
    }
  },
});

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

html.dark .markdown-body .shiki {
  background-color: var(--color-fg-default) !important;
}

.markdown-body .shiki {
  background-color: var(--color-canvas-subtle) !important;
}
</style>
