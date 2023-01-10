<script setup lang="ts">
import type { ProblemRepository } from '@/composables/types';

const props = defineProps<{ repo: ProblemRepository }>();

const { repo } = toRefs(props);

useHead({
  title: `题目设置 - ${repo.value.name}`,
});

const notify = useNotification();

const route = useRoute();

const { data, refresh } = await useFetchAPI<{
  problems: any[];
}>(`/api/repo/${route.params.repo}/problems`);

const problems = computed(() => data.value?.problems ?? []);

const pid = ref(1);

const addProblem = async () => {
  try {
    await fetchAPI<{}>(`/api/repo/${repo.value.id}/problems/add/${pid.value}`, {
      method: 'POST',
    });
    notify.success(`题目添加成功`);
    await refresh();
  } catch (error) {
    notify.danger(`题目添加失败`);
  }
};

const removeProblem = async (pid: number) => {
  try {
    await fetchAPI<{}>(`/api/repo/${repo.value.id}/problems/delete/${pid}`, {
      method: 'POST',
    });
    notify.success(`题目删除成功`);
    await refresh();
  } catch (error) {
    notify.danger(`题目删除失败`);
  }
};
</script>

<template>
  <div w-full>
    <div mb4>
      <c-input type="number" id="pid" v-model="pid">
        <template #label>
          <span font-bold>Polygon 题目编号</span>
        </template>
        <template #end>
          <c-button ml4 color="success" @click="addProblem">添加</c-button>
        </template>
      </c-input>
    </div>
    <problem-list
      :problems="problems"
      :problem-link="
        row => `/repository/${route.params.repo}/problem/${row.display_id}`
      "
    >
      <template #operation="{ row }">
        <c-button
          color="danger"
          variant="text"
          icon="i-carbon-delete"
          @click="removeProblem(row.display_id)"
        ></c-button>
      </template>
    </problem-list>
  </div>
</template>
