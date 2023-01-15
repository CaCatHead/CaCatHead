<script setup lang="ts">
const emit = defineEmits<{
  (e: 'submit', payload: { code: string; language: string }): void;
}>();

const notify = useNotification();

const code = ref('');
const language = ref('cpp');

const submit = async () => {
  if (code.value.length > 65535) {
    notify.danger(`您提交的代码过长`);
  } else {
    emit('submit', { code: code.value, language: language.value });
  }
};
</script>

<template>
  <div space-y-4>
    <slot></slot>
    <problem-select-language v-model="language"></problem-select-language>
    <div w-full>
      <client-only>
        <div font-600 mb2>代码</div>
        <code-editor
          v-model="code"
          :language="language"
          min-h="300px"
        ></code-editor>
        <template #fallback>
          <c-input type="textarea" id="code" v-model="code" font-mono>
            <template #label><span font-600>代码</span></template>
          </c-input>
        </template>
      </client-only>
    </div>
    <div>
      <c-button color="success" w-full @click="submit">提交</c-button>
    </div>
  </div>
</template>
