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

  const list: Array<{ name: string; meta: Record<string, string> }> = [];
  for (const item of result) {
    const add = (key: string) => {
      if (key in item) {
        const name = item[key];
        delete item[key];
        list.push({ name, meta: { ...item } });
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
    </div>
    <div></div>
  </div>
</template>
