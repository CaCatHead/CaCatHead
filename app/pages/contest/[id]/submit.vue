<script setup lang="ts">
import type { FullContest } from '@/composables/types';

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

useHead({
  title: `提交代码 - ${contest.value.title}`,
});

const route = useRoute();
const notify = useNotification();

const lastProblem = useContestLastProblem(route.params.id);

const lastSubmit = useContestLastProblemSubmit(route.params.id);

const problem = ref(lastProblem.value);
const handleSelect = (e: any) => {
  problem.value = +(e?.target?.value ?? 1000);
};

const submit = useThrottleFn(
  async (payload: { code: string; language: string }) => {
    console.log('click');

    const { code, language } = payload;

    const pid = +problem.value;
    lastProblem.value = pid;
    const oldCode = lastSubmit.value[pid];
    if (oldCode === code) {
      notify.warning(`不能连续提交相同代码`);
      return;
    } else {
      lastSubmit.value[pid] = code;
    }

    try {
      await fetchAPI(`/api/contest/${route.params.id}/problem/${pid}/submit`, {
        method: 'POST',
        body: {
          code,
          language,
        },
        notify,
      });
      notify.success(`代码提交成功`);
      await navigateTo(`/contest/${route.params.id}/status`);
    } catch {
      lastSubmit.value[pid] = oldCode;
      notify.danger(`代码提交失败`);
    }
  },
  1000
);
</script>

<template>
  <contest-layout :contest="contest">
    <div>
      <problem-submit @submit="submit">
        <div>
          <label for="problem" font-600 mb2 inline-block>题目</label>
          <c-select id="problem" @click="handleSelect" v-model="problem">
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
