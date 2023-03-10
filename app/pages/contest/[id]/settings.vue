<script setup lang="ts">
import { format, addMinutes } from 'date-fns';

import type { FullContest } from '@/composables/types';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const emit = defineEmits(['refresh-contest']);

const { contest } = toRefs(props);

useHead({
  title: `比赛设置 - ${contest.value.title}`,
});

const formatDatetime = (date: string) => {
  return format(new Date(date), `yyyy-MM-dd'T'HH:mm:SS`);
};

const formatDuration = () => {
  const d = formatInterval(
    new Date(contest.value.start_time),
    new Date(contest.value.end_time)
  );
  const h = d.hours ?? 0;
  const m = d.minutes ?? 0;
  return h * 60 + m;
};

const title = ref(contest.value.title);

const type = ref(contest.value.type);

const start_time = ref(formatDatetime(contest.value.start_time));

const duration = ref(formatDuration());

const description = ref(contest.value.description);

const is_public = ref(contest.value.is_public);
const enable_registering = ref(contest.value?.settings?.enable_registering);
const enable_unregistering = ref(contest.value?.settings?.enable_unregistering);
const view_standings = ref(contest.value?.settings?.view_standings);
const view_submissions_after_contest = ref(
  contest.value?.settings?.view_submissions_after_contest
);
const view_submission_checker_info = ref(
  contest.value?.settings?.view_submission_checker_info
);

const notify = useNotification();

const submit = async () => {
  const start = new Date(start_time.value);
  const end = addMinutes(start, duration.value);

  try {
    await fetchAPI<{ contest: FullContest }>(
      `/api/contest/${route.params.id}/edit`,
      {
        method: 'POST',
        body: {
          title: title.value,
          type: type.value,
          description: description.value,
          start_time: start,
          end_time: end,
          is_public: is_public.value,
          enable_registering: enable_registering.value,
          view_standings: view_standings.value,
          view_submissions_after_contest: view_submissions_after_contest.value,
          view_submission_checker_info: view_submission_checker_info.value,
        },
      }
    );

    contest.value.title = title.value;
    contest.value.description = description.value;
    emit('refresh-contest');

    notify.success(`比赛 ${contest.value.title} 修改成功`);
    await navigateTo(`/contest/${route.params.id}`);
  } catch (err: any) {
    if ('response' in err && typeof err._data?.detail === 'string') {
      notify.danger(err._data?.detail);
    } else {
      notify.danger('未知错误');
    }
    // problems.value = '';
  }
};
</script>

<template>
  <div space-y-4>
    <c-input type="text" id="title" v-model="title">
      <template #label><span font-bold>比赛标题</span></template>
    </c-input>
    <div>
      <div font-bold mb2>比赛类型</div>
      <c-select
        id="type"
        v-model="type"
        :options="['icpc', 'ioi']"
        :empty="false"
      ></c-select>
    </div>
    <c-input type="datetime-local" id="start_time" v-model="start_time">
      <template #label><span font-bold>比赛开始时间</span></template>
    </c-input>
    <c-input type="number" id="duration" v-model="duration">
      <template #label><span font-bold>比赛持续时间 (分钟)</span></template>
    </c-input>
    <hr />
    <div space-y-2 style="--settings-width: 11rem">
      <div flex items-center space-x-4>
        <span font-bold w="$settings-width">是否公开</span>
        <c-switch id="is_public" v-model="is_public"></c-switch>
      </div>
      <div flex items-center space-x-4>
        <span font-bold w="$settings-width">是否允许公开注册</span>
        <c-switch
          id="enable_registering"
          v-model="enable_registering"
        ></c-switch>
      </div>
      <div flex items-center space-x-4>
        <span font-bold w="$settings-width">是否允许取消注册</span>
        <c-switch
          id="enable_unregistering"
          v-model="enable_unregistering"
        ></c-switch>
      </div>
      <div flex items-center space-x-4>
        <span font-bold w="$settings-width">是否开启赛时榜单</span>
        <c-switch id="view_standings" v-model="view_standings"></c-switch>
      </div>
      <div flex items-center space-x-4>
        <span font-bold w="$settings-width">是否开启赛后查看提交</span>
        <c-switch
          id="view_submissions_after_contest"
          v-model="view_submissions_after_contest"
        ></c-switch>
      </div>
      <div flex items-center space-x-4>
        <span font-bold w="$settings-width">是否开启赛后提交详情</span>
        <c-switch
          id="view_submission_checker_info"
          v-model="view_submission_checker_info"
        ></c-switch>
      </div>
    </div>
    <hr />
    <div>
      <h4 mb2 font-bold>比赛描述</h4>
      <markdown-editor v-model="description"></markdown-editor>
    </div>

    <div>
      <c-button color="success" @click="submit">保存</c-button>
    </div>
  </div>
</template>

<style>
.c-select {
  padding-left: 1rem !important;
}
</style>
