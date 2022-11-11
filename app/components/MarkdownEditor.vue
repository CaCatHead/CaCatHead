<script setup lang="ts">
import MdEditor, { type ToolbarNames } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';

const props = withDefaults(
  defineProps<{
    id?: string;
    modelValue: string;
  }>(),
  {
    id: () => 'markdown-editor-' + randomString(),
  }
);

const emit = defineEmits(['update:modelValue']);

const data = useVModel(props, 'modelValue', emit);

const toolbars: ToolbarNames[] = [
  'bold',
  'underline',
  'italic',
  '-',
  'katex',
  'link',
  'image',
  'table',
  'codeRow',
  'code',
  '-',
  'strikeThrough',
  'title',
  // 'sub',
  // 'sup',
  'quote',
  'unorderedList',
  'orderedList',
  'task', // ^2.4.0
  // 'mermaid',
  '-',
  'revoke',
  'next',
  // 'save',
  '=',
  'pageFullscreen',
  'fullscreen',
  'preview',
  'htmlPreview',
];
</script>

<template>
  <md-editor
    v-model="data"
    :preview="false"
    :toolbars="toolbars"
    :editor-id="id"
    rounded-2
  />
</template>
