<script setup lang="ts">
import * as clipboard from 'clipboard-polyfill';

import { highlight } from '@/composables/highlight';

const notify = useNotification();

const props = withDefaults(
  defineProps<{ code?: string; language?: string; copy?: boolean }>(),
  {
    code: '',
    language: 'cpp',
    copy: true,
  }
);

const { code, language, copy } = toRefs(props);

const isDark = useDark();

function hash(s: string) {
  let h = 0,
    l = s.length,
    i = 0;
  if (l > 0) while (i < l) h = ((h << 5) - h + s.charCodeAt(i++)) | 0;
  return h;
}

const renderCacheLight = useLocalStorage(
  'render/cache/light',
  {} as Record<string, { c: string; r: string; f: boolean }>
);
const renderCacheDark = useLocalStorage(
  'render/cache/dark',
  {} as Record<string, { c: string; r: string; f: boolean }>
);

const isHydrating = !!useNuxtApp().isHydrating;

const settings = ref({
  tabwidth: 2,
  format: true,
});

const rendered = computed(() => {
  const renderCache = isDark ? renderCacheDark.value : renderCacheLight.value;
  const hsh = hash(code.value);
  // Hyration 的时候，不能读取缓存
  if (
    !isHydrating &&
    hsh in renderCache &&
    renderCache[hsh].c === code.value &&
    renderCache[hsh].f === settings.value.format
  ) {
    return renderCache[hsh].r;
  } else {
    const result = highlight(code.value, language.value, settings.value);
    if (language.value === result.language) {
      renderCache[hsh] = {
        c: code.value,
        r: result.html,
        f: result.option.format,
      };
    }
    return result.html;
  }
});

const line = computed(() => {
  return code.value.split('\n').length;
});
const measure = ref<HTMLElement | null>(null);
const width = computed(() => {
  if (measure.value) {
    return measure.value.clientWidth + 2 + 'px';
  } else {
    return '1em';
  }
});

const copyToClipboard = async () => {
  try {
    await clipboard.writeText(code.value);
  } catch {
    notify.danger(`代码复制失败`);
  }
};
</script>

<template>
  <div v-show="rendered.length > 0" class="code-box relative transition-all">
    <div absolute top-2 right-2 lt-md="top-0 right-1" v-if="copy">
      <c-button
        variant="text"
        color="success"
        lt-sm="text-xs"
        @click="settings.format = !settings.format"
        >{{ settings.format ? '源文件' : '格式化' }}</c-button
      >
      <c-button
        variant="text"
        color="info"
        lt-sm="text-xs"
        @click="copyToClipboard"
        >复制</c-button
      >
    </div>
    <div
      :class="['px-4 py-4 min-h-14 overflow-x-auto lt-md:text-xs lt-md:p-2']"
      v-html="rendered"
    ></div>
    <div class="hidden-measure font-mono lt-md:text-xs" ref="measure">
      {{ line + 1 }}
    </div>
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
  --at-apply: lt-sm:pr4;
  height: 1em;
  line-height: 1em;
}

.ml-md {
  margin-left: 1rem;
}

.code-box .ml-token {
  margin-left: calc(v-bind(width) + 0.5em);
}

.code-box .shiki code .line::before {
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
  .code-box .ml-token {
    margin-left: calc(v-bind(width) + 1em);
  }

  .code-box .shiki code .line::before {
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
