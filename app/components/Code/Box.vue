<script setup lang="ts">
import { highlight } from '@/composables/highlight';

const props = withDefaults(
  defineProps<{ code?: string; language?: string; copy?: boolean }>(),
  {
    code: '',
    language: 'cpp',
    copy: true,
  }
);

const { code, language, copy } = toRefs(props);

const rendered = ref('');

const isDark = useDark();

function hash(s: string) {
  let h = 0,
    l = s.length,
    i = 0;
  if (l > 0) while (i < l) h = ((h << 5) - h + s.charCodeAt(i++)) | 0;
  return h;
}

const renderCache = useLocalStorage(
  'render/cache',
  {} as Record<string, { c: string; r: string }>
);

const isHydrating = !!useNuxtApp().isHydrating;

watch(
  () => [code.value, language.value, isDark.value] as [string, string, boolean],
  async ([code, language, isDark]) => {
    const hsh = hash(code);
    // Hyration 的时候，不能读取缓存
    if (
      !isHydrating &&
      hsh in renderCache.value &&
      renderCache.value[hsh].c === code
    ) {
      rendered.value = renderCache.value[hsh].r;
    } else {
      const result = await highlight(code, language, isDark);
      rendered.value = result;
      renderCache.value[hsh] = { c: code, r: result };
    }
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

const copyToClipboard = async () => {
  await navigator.clipboard.writeText(code.value);
};
</script>

<template>
  <div v-show="rendered.length > 0" class="code-box relative transition-all">
    <div absolute top-2 right-2 v-if="copy">
      <c-button variant="text" color="info" @click="copyToClipboard"
        >复制</c-button
      >
    </div>
    <div
      :class="['px-4 py-4 min-h-14 overflow-x-auto lt-md:text-xs lt-md:p-2']"
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
