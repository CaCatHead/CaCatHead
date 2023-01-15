<script setup lang="ts">
import { highlight } from '@/composables/highlight';

const props = withDefaults(
  defineProps<{ code?: string; language?: string }>(),
  {
    code: '',
    language: 'cpp',
  }
);

const { code, language } = toRefs(props);

const rendered = ref('');

const isDark = useDark();

watch(
  () => [code.value, language.value, isDark.value],
  async () => {
    rendered.value = await highlight(code.value, language.value, isDark.value);
  },
  { immediate: true }
);

const measure = ref<HTMLElement | null>(null);
const width = computed(() => {
  if (measure.value) {
    return measure.value.clientWidth + 2 + 'px';
  } else {
    return '1em';
  }
});
</script>

<template>
  <div class="code-box">
    <div
      :class="['px-4 py-4 overflow-x-auto lt-md:text-xs lt-md:p-2']"
      v-html="rendered"
    ></div>
  </div>
</template>

<style>
.code-box {
  --at-apply: rounded border-1 border-base;
  tab-size: 2;
}

.shiki {
  margin: 0;
  background-color: white !important;
}

html.dark .shiki {
  background-color: #222 !important;
}

.markdown-body .shiki {
  background-color: var(--color-canvas-subtle) !important;
}

.shiki code {
  counter-reset: step;
  counter-increment: step 0;
}

.shiki code .line {
  height: 1em;
  line-height: 1em;
}

.ml-md {
  margin-left: 1rem;
}

.code-box .markdown-body {
  margin-left: 1rem;
  margin-right: 1rem;
  margin-bottom: 1rem;
}

.ml-token {
  margin-left: calc(v-bind(width) + 0.5em);
}

.shiki code .line::before {
  content: counter(step);
  counter-increment: step;
  height: 1em;
  width: v-bind(width);
  line-height: 1em;
  margin-right: 0.5em;
  display: inline-block;
  text-align: right;
  color: rgba(115, 138, 148, 0.4);
}

@media (min-width: 768px) {
  .ml-token {
    margin-left: calc(v-bind(width) + 1em);
  }
  .shiki code .line::before {
    margin-right: 1em;
  }
}

.hidden-measure {
  position: absolute;
  visibility: hidden;
  height: auto;
  width: auto;
  white-space: nowrap;
}
</style>
