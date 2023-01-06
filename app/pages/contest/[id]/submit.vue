<script setup lang="ts">
import type { FullContest } from '@/composables/types';

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `提交代码 - ${contest.value.title}`,
});

const route = useRoute();
const notify = useNotification();

const lastProblem = useLocalStorage(
  `contest/${route.params.id}/last-problem`,
  1000
);

const problem = ref(lastProblem.value);
const handleSelect = (e: any) => {
  problem.value = e?.target?.value ?? 1000;
};

const submit = async (payload: { code: string; language: string }) => {
  const { code, language } = payload;
  try {
    await fetchAPI(
      `/api/contest/${route.params.id}/problem/${problem.value}/submit`,
      {
        method: 'POST',
        body: {
          code,
          language,
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
  <contest-layout :contest="contest">
    <div>
      <problem-submit @submit="submit">
        <div>
          <label for="problem" font-600 mb2 inline-block>题目</label>
          <c-select id="problem" @click="handleSelect">
            <option
              v-for="p in contest.problems"
              :value="p.display_id"
              :selected="problem === p.display_id"
            >
              {{ displyaIdToIndex(p.display_id) }}. {{ p.title }}
            </option>
          </c-select>
        </div>
      </problem-submit>
    </div>
  </contest-layout>
</template>
