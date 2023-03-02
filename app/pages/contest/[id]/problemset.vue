<script setup lang="ts">
import type {
  FullContest,
  ContestExtraInfo,
  Problem,
  FullPolygonProblem,
} from '@/composables/types';

const route = useRoute();

const notify = useNotification();

const props = defineProps<{
  contest: FullContest;
  extra_info: ContestExtraInfo | null;
}>();

const { contest } = toRefs(props);

const extra_info = props.extra_info;

useHead({
  title: `题目列表设置 - ${contest.value.title}`,
});

const pid = ref(1);

const problems = ref(
  [...contest.value.problems].map((p, idx) => ({
    polygon_id: unref(extra_info?.polygon_problems?.[idx].id) ?? -1,
    ...p,
  }))
);

const addProblem = async () => {
  try {
    const oldProblem = problems.value.find(p => p.polygon_id === +pid.value);
    if (!!oldProblem) {
      notify.danger(
        `题目 #${oldProblem.polygon_id}. ${oldProblem.title} 已经被添加`
      );
      pid.value += 1;
      return;
    }

    const { problem } = await fetchAPI<{ problem: FullPolygonProblem }>(
      `/api/polygon/${pid.value}`
    );
    problems.value.push({ polygon_id: problem.display_id, ...problem });
    notify.success(`题目 #${problem.display_id}. ${problem.title} 查询成功`);

    pid.value += 1;
  } catch (error: any) {
    console.error(error);
    notify.danger(`题目 #${pid.value}. 查询失败`);
  }
};

const removeProblem = (_row: Problem, index: number) => {
  if (index < problems.value.length) {
    problems.value.splice(index, 1);
  }
};

const prepareProblem = useThrottleFn(async (row: Problem, _index: number) => {
  try {
    if (!!problems.value.find(p => p.polygon_id === -1)) {
      return;
    }

    await fetchAPI<{ contest: FullContest }>(
      `/api/contest/${route.params.id}/problem/${row.display_id}/prepare`,
      {
        method: 'POST',
        body: {
          code: [`#include <cstdio>`, `int main() { return 0; }`].join('\n'),
          language: 'cpp',
        },
      }
    );

    notify.success(
      `题目 ${displyaIdToIndex(row.display_id)}. ${row.title} 开始预热`
    );
  } catch (err: any) {
    notify.danger(
      `题目 ${displyaIdToIndex(row.display_id)}. ${row.title} 发起预热失败`
    );
  }
}, 1000);

const save = async () => {
  try {
    if (!!problems.value.find(p => p.polygon_id === -1)) {
      return;
    }

    await fetchAPI<{ contest: FullContest }>(
      `/api/contest/${route.params.id}/edit`,
      {
        method: 'POST',
        body: {
          problems: problems.value.map(p => p.polygon_id),
        },
      }
    );

    notify.success(`比赛 ${contest.value.title} 题目列表修改成功`);
    await navigateTo(`/contest/${route.params.id}`);
  } catch (err: any) {
    if ('response' in err) {
      notify.danger(err.data.detail);
    } else {
      notify.danger('未知错误');
    }
  }
};
</script>

<template>
  <div space-y-4>
    <div>
      <c-input type="number" id="pid" v-model="pid">
        <template #label>
          <span font-bold>Polygon 题目编号</span>
        </template>
        <template #end>
          <c-button ml4 color="success" variant="outline" @click="addProblem"
            >添加</c-button
          >
        </template>
      </c-input>
    </div>
    <problem-list
      :problems="problems"
      :problem-index="(_row, index) => displyaIdToIndex(index)"
      :problem-link="
        row =>
          `/contest/${route.params.id}/problem/${displyaIdToIndex(
            row.display_id
          )}`
      "
      operation-width="100px"
    >
      <template #operation="{ row, index }">
        <c-button
          color="warning"
          variant="text"
          icon="i-carbon-fire"
          @click="prepareProblem(row, index)"
        ></c-button>
        <c-button
          color="danger"
          variant="text"
          icon="i-carbon-delete"
          @click="removeProblem(row, index)"
        ></c-button>
      </template>
    </problem-list>
    <div w-full>
      <c-button color="success" w-full @click="save">保存</c-button>
    </div>
  </div>
</template>
