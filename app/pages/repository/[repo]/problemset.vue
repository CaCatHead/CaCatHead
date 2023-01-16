<script setup lang="ts">
import type { ProblemRepository, Problem } from '@/composables/types';

const props = defineProps<{ repo: ProblemRepository }>();

const { repo } = toRefs(props);

useHead({
  title: `题目列表设置 - ${repo.value.name}`,
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

const removeProblem = async (problem: Problem) => {
  try {
    await fetchAPI<{}>(
      `/api/repo/${repo.value.id}/problems/delete/${problem.display_id}`,
      {
        method: 'POST',
      }
    );
    notify.success(`题目删除成功`);
    await refresh();
  } catch (error) {
    notify.danger(`题目删除失败`);
  }
};

const toggleProblemPublic = async (problem: Problem) => {
  const mode = problem.is_public ? '隐藏' : '公开';
  try {
    await fetchAPI<{}>(
      `/api/repo/${repo.value.id}/problem/${problem.display_id}/edit`,
      {
        method: 'POST',
        body: {
          is_public: !problem.is_public,
        },
      }
    );
    notify.success(`题目${mode}成功`);
    await refresh();
  } catch (error) {
    notify.danger(`题目${mode}失败`);
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
      operation-width="100px"
    >
      <template #operation="{ row }">
        <c-button
          color="info"
          variant="text"
          :icon="row.is_public ? 'i-carbon-view' : 'i-carbon-view-off'"
          @click="toggleProblemPublic(row)"
        ></c-button>
        <c-button
          color="danger"
          variant="text"
          icon="i-carbon-delete"
          @click="removeProblem(row)"
        ></c-button>
      </template>
    </problem-list>
  </div>
</template>
