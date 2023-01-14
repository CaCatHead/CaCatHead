<script setup lang="ts">
import ace, { type Ace } from 'ace-builds';

// @ts-ignore
import CppUrl from 'ace-builds/src-noconflict/mode-c_cpp?url';
// @ts-ignore
import JavaUrl from 'ace-builds/src-noconflict/mode-java?url';

ace.config.setModuleUrl('ace/mode/c_cpp', CppUrl);
ace.config.setModuleUrl('ace/mode/java', JavaUrl);

const props = withDefaults(
  defineProps<{
    modelValue: string;
    placeholder?: string;
    language?: string;
    readonly?: boolean;
    minLines?: number;
    maxLines?: number;
    theme?: string;
    options?: Partial<Ace.EditorOptions>;
  }>(),
  {
    placeholder: '',
    language: 'cpp',
    readonly: false,
    minLines: undefined,
    maxLines: undefined,
    theme: '',
    options: () => ({}),
  }
);

const {
  placeholder,
  language: _language,
  readonly,
  minLines,
  maxLines,
  theme,
  options,
} = toRefs(props);

const language = computed(() => {
  if (_language.value === 'c' || _language.value === 'cpp') {
    return 'c_cpp';
  } else {
    return _language.value;
  }
});

const emit = defineEmits(['update:modelValue']);

const data = useVModel(props, 'modelValue', emit);

const element = ref();
const editor = ref();

const isSettingContent = ref(false);
const contentBackup = ref<string>();
watch(data, data => {
  if (editor.value) {
    if (contentBackup.value !== data) {
      try {
        isSettingContent.value = true;
        editor.value.setValue(data, 1);
      } finally {
        isSettingContent.value = false;
      }
      contentBackup.value = data;
    }
  }
});
watch(language, language => {
  if (editor.value && language) {
    editor.value.session.setMode('ace/mode/' + language);
  }
});

onMounted(() => {
  if (process.server) {
    return;
  }
  if (element.value) {
    editor.value = ace.edit(element.value, {
      placeholder: placeholder.value,
      readOnly: readonly.value,
      value: data.value,
      mode: 'ace/mode/' + language.value,
      theme: theme.value ? 'ace/theme/' + theme.value : undefined,
      useWorker: false,
      minLines: minLines.value,
      maxLines: maxLines.value,
      fontSize: 16,
      ...options.value,
    });
    editor.value.on('change', () => {
      if (isSettingContent.value) return;
      const content = editor.value.getValue();
      contentBackup.value = content;
      data.value = editor.value.getValue();
    });
  }
});
</script>

<template>
  <div ref="element" border="1 base"></div>
</template>
