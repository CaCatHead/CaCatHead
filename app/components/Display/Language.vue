<script setup lang="ts">
const props = withDefaults(defineProps<{ language: string }>(), {
  language: 'cpp',
});

const { language } = toRefs(props);

const LANG_MAP: Record<string, string> = {
  c: 'C',
  cpp: 'C++',
  java: 'Java',
};
</script>

<template>
  <span v-if="language in LANG_MAP">{{ LANG_MAP[language] }}</span>
  <span v-else>{{ language }}</span>
</template>
