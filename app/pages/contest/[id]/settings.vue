<script setup lang="ts">
import type { FullContest } from '@/composables/types';
import { format, addMinutes } from 'date-fns';

const route = useRoute();

const props = defineProps<{ contest: FullContest }>();

const { contest } = toRefs(props);

const title = ref(contest.value.title);

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

const start_time = ref(formatDatetime(contest.value.start_time));

const duration = ref(formatDuration());

const notify = useNotification();

const submit = async () => {
  const start = new Date(start_time.value);
  const end = addMinutes(start, duration.value);

  await fetchAPI(`/api/contest/${route.params.id}/edit`, {
    method: 'POST',
    body: {
      title: title.value,
      start_time: start,
      end_time: end,
    },
  });

  contest.value.title = title.value;

  notify.success(`比赛 ${contest.value.title} 修改成功`);
};
</script>

<template>
  <div space-y-4>
    <c-input type="text" id="title" v-model="title">
      <template #label>比赛标题</template>
    </c-input>
    <c-input type="datetime-local" id="start_time" v-model="start_time">
      <template #label>比赛开始时间</template>
    </c-input>
    <c-input type="number" id="duration" v-model="duration">
      <template #label>比赛持续时间 (分钟)</template>
    </c-input>

    <div>
      <c-button color="success" @click="submit">保存</c-button>
    </div>
  </div>
</template>
