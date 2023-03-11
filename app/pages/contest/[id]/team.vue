<script setup lang="ts">
import type { FullContest, ContestExtraInfo } from '@/composables/types';

import { parse } from 'csv-parse/browser/esm/sync';

const route = useRoute();

const notify = useNotification();

const props = defineProps<{
  contest: FullContest;
  extra_info: ContestExtraInfo | null;
}>();

const { contest } = toRefs(props);

const file = ref([] as File[]);

const uploadTeams = async () => {
  if (file.value.length < 1) return;
  const csv = file.value[0];
  const content = new TextDecoder('utf-8', { ignoreBOM: false }).decode(
    await readFileToU8(csv)
  );
  const result = parse(content, {
    encoding: 'utf-8',
    columns: true,
    skip_empty_lines: true,
    trim: true,
  }) as any[];

  const list: Array<{
    team: string;
    username: string;
    password: string;
    meta: Record<string, string>;
  }> = [];
  for (const item of result) {
    const add = (key: string) => {
      if (key in item) {
        const team = item[key];
        const username = item['用户名'] ?? `contest${route.params.id}_${team}`;
        const password = item['密码'];
        delete item[key];
        delete item['用户名'];
        delete item['密码'];
        list.push({ team, username, password, meta: { ...item } });
        return true;
      } else {
        return false;
      }
    };

    add('队名') ||
      add('队伍') ||
      add('姓名') ||
      add('学号') ||
      add('名称') ||
      add('名字');
  }

  await fetchAPI(`/api/contest/${route.params.id}/registrations/import`, {
    method: 'POST',
    body: {
      registrations: list,
    },
    notify,
  });

  notify.success(`成功导入 ${list.length} 支队伍`);
  await navigateTo(`/contest/${route.params.id}/standings`);
};
</script>

<template>
  <div>
    <div space-x-2>
      <c-file-input
        id="teams"
        v-model="file"
        accept=".csv"
        @change="uploadTeams"
        >导入队伍列表</c-file-input
      >
      <c-button
        tag="a"
        color="info"
        :download="`${contest.title} 榜单.csv`"
        :href="`/api/contest/${route.params.id}/standings/export`"
        >导出榜单</c-button
      >
    </div>
    <div></div>
  </div>
</template>
