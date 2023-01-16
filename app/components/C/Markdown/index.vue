<script setup lang="ts">
import 'katex/dist/katex.min.css';

import type { Highlighter } from 'shiki-es';

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

const highlighter = ref<Highlighter>();

if (!process.server) {
  preSetup()
    .then(hl => {
      highlighter.value = hl;
    })
    .catch(error => {
      console.error(error);
      return undefined;
    });
}

const render = createMarkdown({
  highlight: (code, lang) => {
    code = code.trim();
    lang = alias.get(lang) ?? lang;
    if (highlighter.value && isLangSupport(lang)) {
      console.log(isDark.value);
      return highlighter.value.codeToHtml(code, {
        lang,

        theme: isDark.value ? 'Eva Dark' : 'Eva Light',
      });
    } else {
      return escapeCode(code);
    }
  },
});

const result = computed(() => {
  // Track deps
  let _deps = highlighter.value && isDark.value;
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
