<script setup lang="ts">
const route = useRoute();
const notify = useNotification();

const problem = ref(1000);
const code = ref('');
const language = ref('cpp');

const submit = async () => {
  try {
    await fetchAPI(
      `/api/contest/${route.params.id}/problem/${problem.value}/submit`,
      {
        method: 'POST',
        body: {
          code: code.value,
          language: language.value,
        },
      }
    );
    notify.success(`代码提交成功`);
    await navigateTo(`/contest/${route.params.id}/status`);
  } catch {
    notify.danger(`代码提交失败`);
  }
};
</script>

<template>
  <div>
    <div>
      <c-input type="text" id="problem" v-model="problem">
        <template #label>
          <span font-600>题目</span>
        </template>
      </c-input>
    </div>
    <div>
      <span mr2 font-600>语言:</span>
      <span>C++</span>
    </div>
    <c-input type="textarea" id="code" v-model="code" font-mono>
      <template #label><span></span></template>
    </c-input>
    <div>
      <c-button color="success" w-full @click="submit">提交</c-button>
    </div>
  </div>
</template>
